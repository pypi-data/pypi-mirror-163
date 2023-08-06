# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Define the grad rules of math related operations."""

from mindspore.common import dtype as mstype
from mindspore import nn
import mindspore.numpy as mnp
import numpy as np
from .. import functional as F
from .. import operations as P
from ..operations.math_ops import Trace, Bernoulli, Renorm
from ..operations.math_ops import Real, Imag, Complex, Angle
from ..functional import broadcast_gradient_args
from .._grad.grad_base import bprop_getters
from .._grad.grad_math_ops import binop_grad_common
from ..composite.multitype_ops.zeros_like_impl import zeros_like
from ..operations import _grad_ops as G
from ..operations import math_ops as math
from ..operations.math_ops import Igamma, Igammac
from ..primitive import constexpr
from ..operations.math_ops import Hypot
from ..operations.math_ops import ReduceStd
from ..operations.math_ops import CholeskySolve
from ..operations.math_ops import AddV2

transpose = P.Transpose()


@constexpr
def _generate_perm(x_dim):
    perm = tuple(range(x_dim - 2))
    return perm


@bprop_getters.register(P.ACos)
def get_bprop_acos(self):
    """Grad definition for `ACos` operation."""
    input_grad = G.ACosGrad()

    def bprop(input_x, out, dout):
        dx = input_grad(input_x, dout)
        return (dx,)

    return bprop


@bprop_getters.register(P.Cdist)
def get_bprop_cdist(self):
    """Generate bprop for Cdist"""
    input_grad = G.CdistGrad(p=self.p)

    def bprop(input_x, input_y, out, dout):
        dout_shape = F.shape(dout)
        dout_dim = len(dout_shape)
        dout_perm_part1 = _generate_perm(dout_dim)
        dout_perm_part2 = (dout_dim - 1, dout_dim - 2)
        dout_perm = dout_perm_part1 + dout_perm_part2
        out_perm = dout_perm
        dout_transpose = transpose(dout, dout_perm)
        out_transpose = transpose(out, out_perm)
        dx = input_grad(dout, input_x, input_y, out)
        dy = input_grad(dout_transpose, input_y, input_x, out_transpose)
        return dx, dy

    return bprop


@bprop_getters.register(P.Lerp)
def get_bprop_index_lerp(self):
    """Generate bprop for Lerp"""
    mul_op = P.Mul()
    sub_op = P.Sub()
    is_instance_op = P.IsInstance()

    def bprop(start, end, weight, out, dout):
        dout = F.cast(dout, mstype.float32)
        dstart = mul_op(dout, 1 - weight)
        dend = mul_op(dout, weight)
        dweight = mul_op(dout, sub_op(end, start))
        dstart, dend = binop_grad_common(start, end, dstart, dend)
        if is_instance_op(weight, mstype.number):
            dweight = 0
        else:
            _, dweight = binop_grad_common(start, weight, dstart, dweight)
            dweight = F.cast(dweight, F.dtype(weight))
        dstart = F.cast(dstart, F.dtype(start))
        dend = F.cast(dend, F.dtype(end))
        return dstart, dend, dweight

    return bprop


@bprop_getters.register(ReduceStd)
def get_bprop_reduce_std(self):
    """Grad definition for `ReduceStd` operation."""
    axis = list(self.axis)
    keep_dims = self.keep_dims
    unbiased = self.unbiased
    expand_dims_op = P.ExpandDims()
    size_op = P.Size()
    mul_op = P.Mul()
    sub_op = P.Sub()
    div_op = P.Div()
    add_op = P.Add()

    def bprop(x, out, dout):
        std_d = dout[0]
        std = out[0]
        mean_d = dout[1]
        mean = out[1]
        if axis == [] and x.shape != ():
            for i, _ in enumerate(x.shape):
                axis.append(i)
        for i, _ in enumerate(axis):
            if axis[i] < 0:
                axis[i] = axis[i] + len(x.shape)
        for i in range(1, len(axis)):
            for j in range(0, len(axis) - i):
                if axis[j] > axis[j + 1]:
                    axis[j], axis[j + 1] = axis[j + 1], axis[j]
        if not keep_dims and x.shape != ():
            for i in axis:
                std_d = expand_dims_op(std_d, i)
                std = expand_dims_op(std, i)
                mean_d = expand_dims_op(mean_d, i)
                mean = expand_dims_op(mean, i)
        dx = sub_op(x, mean)
        dx = mul_op(dx, std_d)
        dx = div_op(dx, std)
        num = size_op(x)
        for i, _ in enumerate(x.shape):
            if i not in axis:
                num = num / x.shape[i]
        if unbiased:
            dx = div_op(dx, num - 1)
        else:
            dx = div_op(dx, num)
        temp = div_op(mean_d, num)
        dx = add_op(dx, temp)
        return (dx,)

    return bprop


@bprop_getters.register(P.Addcdiv)
def get_bprop_index_addcdiv(self):
    """Generate bprop for Addcdiv"""
    mul_op = P.Mul()
    div_op = P.Div()
    pow_op = P.Pow()
    neg_op = P.Neg()

    def bprop(input_data, x1, x2, value, out, dout):
        dinput_data = dout
        if dout.dtype in [mstype.float16, mstype.int64, mstype.float64]:
            input_data = F.cast(input_data, mstype.float32)
            x1 = F.cast(x1, mstype.float32)
            x2 = F.cast(x2, mstype.float32)
            value = F.cast(value, mstype.float32)
            dinput_data = F.cast(dinput_data, mstype.float32)
        inner_out = mul_op(value, div_op(x1, x2)) + input_data
        dx2 = neg_op(mul_op(mul_op(mul_op(x1, value), pow_op(x2, -2)), dinput_data))
        dx1 = mul_op(dinput_data, div_op(value, x2))
        dvalue = mul_op(dinput_data, div_op(x1, x2))
        _, dinput_data = binop_grad_common(inner_out, input_data, dinput_data, dinput_data)
        _, dx1 = binop_grad_common(inner_out, x1, dinput_data, dx1)
        _, dx2 = binop_grad_common(inner_out, x2, dinput_data, dx2)
        _, dvalue = binop_grad_common(inner_out, value, dinput_data, dvalue)
        if dout.dtype in [mstype.float16, mstype.int64, mstype.float64]:
            dinput_data = F.cast(dinput_data, dout.dtype)
            dx1 = F.cast(dx1, dout.dtype)
            dx2 = F.cast(dx2, dout.dtype)
            dvalue = F.cast(dvalue, dout.dtype)

        return dinput_data, dx1, dx2, dvalue

    return bprop


@bprop_getters.register(P.Addcmul)
def get_bprop_index_addcmul(self):
    """Generate bprop for Addcmul"""
    mul_op = P.Mul()

    def bprop(input_data, x1, x2, value, out, dout):
        if dout.dtype in [mstype.float16, mstype.float64, mstype.uint8, mstype.int8]:
            input_data = F.cast(input_data, mstype.float32)
            x1 = F.cast(x1, mstype.float32)
            x2 = F.cast(x2, mstype.float32)
            value = F.cast(value, mstype.float32)
        dinput_data = dout
        dx1 = mul_op(dout, mul_op(value, x2))
        dx2 = mul_op(dout, mul_op(value, x1))
        inner_out = mul_op(x1, x2) * value + input_data
        dvalue = mul_op(dout, mul_op(x1, x2))
        _, dinput_data = binop_grad_common(inner_out, input_data, dout, dinput_data)
        _, dx1 = binop_grad_common(inner_out, x1, dout, dx1)
        _, dx2 = binop_grad_common(inner_out, x2, dout, dx2)
        _, dvalue = binop_grad_common(inner_out, value, dout, dvalue)
        if dout.dtype in [mstype.float16, mstype.uint8, mstype.int8, mstype.float64]:
            dinput_data = F.cast(dinput_data, dout.dtype)
            dx1 = F.cast(dx1, dout.dtype)
            dx2 = F.cast(dx2, dout.dtype)
            dvalue = F.cast(dvalue, dout.dtype)
        return dinput_data, dx1, dx2, dvalue

    return bprop


@constexpr
def renew_dim(shape, dim):
    """ Re-new dims"""
    new_dim = dim if dim >= 0 else len(shape) + dim
    tmp = [i for i in range(len(shape))]
    _ = tmp.pop(new_dim)
    return tuple(tmp)


@bprop_getters.register(Renorm)
def get_bprop_renorm(self):
    """Generate bprop for Renorm """
    p = int(self.p)
    ext = 1e-7
    dim = self.dim
    max_norm = self.maxnorm
    greater_op = P.Greater()
    masked_fill_op = P.MaskedFill()
    pow_op = P.Pow()
    abs_op = P.Abs()
    sign_op = P.Sign()
    reciprocal_op = P.Reciprocal()

    def bprop(input_x, out, dout):
        shape = F.shape(input_x)
        dims = renew_dim(shape, dim)
        norm = P.LpNorm(dims, p, keep_dims=True)(input_x)
        grad_out = (input_x * dout)
        grad_out = grad_out.sum(dims, keepdims=True)
        if p == 1:
            sig = sign_op(input_x)
            norm_bp = sig * grad_out
        elif p == 2:
            m = input_x * (grad_out / norm)
            norm_bp = masked_fill_op(m, norm == 0., 0.)
        else:
            abs_ = abs_op(input_x)
            input_scaled = input_x * pow_op(abs_, (p - 2))
            pow_ = pow_op(norm, (p - 1))
            scale_v = grad_out / pow_
            scale_v = masked_fill_op(scale_v, norm == 0., 0.)
            norm_bp = input_scaled * scale_v

        v = norm + ext
        inv_norm = reciprocal_op(v)
        grad_norm = max_norm * inv_norm * (dout - inv_norm * norm_bp)
        q = greater_op(norm, max_norm)
        return (mnp.where(q, grad_norm, dout),)

    return bprop


@bprop_getters.register(P.LpNorm)
def get_bprop_lp_norm(self):
    """Grad definition for `LpNorm` operation."""
    p = self.p
    keep_dims = self.keep_dims
    axis = self.axis
    if isinstance(axis, int):
        axis = [axis]
    sign_op = P.Sign()
    abs_op = P.Abs()
    zeros_like_op = P.ZerosLike()
    expand_dims_op = P.ExpandDims()
    pow_op = P.Pow()

    def bprop(input_x, out, dout):
        if not keep_dims and input_x.shape != ():
            for i in axis:
                dout = expand_dims_op(dout, i)
                out = expand_dims_op(out, i)

        if p == 0:
            return (zeros_like_op(input_x),)
        if p == 1:
            return (dout * sign_op(input_x),)
        if p == 2:
            input_scaled = input_x
            scale_v = dout / out
        else:
            input_scaled = pow_op(abs_op(input_x), (p - 2)) * input_x
            scale_v = dout / pow_op(out, (p - 1))
        return (input_scaled * scale_v,)

    return bprop


@bprop_getters.register(P.MatrixInverse)
def get_bprop_matrix_inverse(self):
    """Generate bprop for MatrixInverse"""
    matmul_x1 = nn.MatMul(transpose_x1=True)
    matmul_x2 = nn.MatMul(transpose_x2=True)
    neg = P.Neg()

    def bprop(x, out, dout):
        dx = matmul_x2(dout, out)
        dx = matmul_x1(out, dx)
        dx = neg(dx)
        return (dx,)

    return bprop


@bprop_getters.register(P.MatrixDeterminant)
def get_bprop_matrix_determinant(self):
    """Generate bprop for MatrixDeterminant"""
    inverse_op = P.MatrixInverse(adjoint=True)
    shape_op = P.Shape()
    reshape = P.Reshape()

    def bprop(x, out, dout):
        x_adj_inv = inverse_op(x)
        multipliers = reshape(dout * out, shape_op(out) + (1, 1))
        dx = multipliers * x_adj_inv
        return (dx,)

    return bprop


@bprop_getters.register(P.LogMatrixDeterminant)
def get_bprop_log_matrix_determinant(self):
    """Generate bprop for LogMatrixDeterminant"""
    inverse_op = P.MatrixInverse(adjoint=True)
    shape_op = P.Shape()
    reshape = P.Reshape()

    def bprop(x, out, dout):
        x_adj_inv = inverse_op(x)
        multipliers = reshape(dout[1], shape_op(out[1]) + (1, 1))
        dx = multipliers * x_adj_inv
        return (dx,)

    return bprop


@bprop_getters.register(P.CholeskyInverse)
def get_bprop_cholesky_inverse(self):
    """Grad definition for `CholeskyInverse` operation."""
    matmul = P.MatMul()
    upper = self.upper
    neg = P.Neg()

    def bprop(input_x, out, dout):
        input_perm = (1, 0)
        if dout.dtype == mstype.float64:
            input_x = F.cast(input_x, mstype.float32)
            out = F.cast(out, mstype.float32)
            dout = F.cast(dout, mstype.float32)
            common_term = dout + transpose(dout, input_perm)
            common_term = F.cast(common_term, mstype.float32)
            common_term = matmul(out, matmul(common_term, out))
            if upper is True:
                dx = neg(matmul(input_x, common_term))
                dx = F.cast(dx, mstype.float64)
            else:
                dx = neg(matmul(common_term, input_x))
                dx = F.cast(dx, mstype.float64)
            return (dx,)
        common_term = dout + transpose(dout, input_perm)
        common_term = matmul(out, matmul(common_term, out))
        if upper is True:
            dx = neg(matmul(input_x, common_term))
        else:
            dx = neg(matmul(common_term, input_x))
        return (dx,)

    return bprop


@bprop_getters.register(Real)
def get_bprop_real(self):
    """Grad definition for `Real` operation."""
    complex_grad = Complex()

    def bprop(input_1, out, dout):
        zero = zeros_like(dout)
        dx = dout
        res = complex_grad(dx, zero)
        return (res,)

    return bprop


@bprop_getters.register(Imag)
def get_bprop_imag(self):
    """Grad definition for `Real` operation."""
    complex_grad = Complex()

    def bprop(input_1, out, dout):
        zero = zeros_like(dout)
        dx = dout
        res = complex_grad(zero, dx)
        return (res,)

    return bprop


@bprop_getters.register(Complex)
def get_bprop_complex(self):
    """Grad definition for `Real` operation."""
    real_grad = Real()
    imag_grad = Imag()

    def bprop(real, imag, out, dout):
        dx = real_grad(dout)
        dy = imag_grad(dout)
        return (dx, dy,)

    return bprop


@bprop_getters.register(Angle)
def get_bprop_angle(self):
    """Grad definition for `Angle` operation."""
    real_op = Real()
    imag_op = Imag()
    reciprocal_op = P.Reciprocal()
    complex_op = Complex()
    neg_op = P.Neg()

    def bprop(x, out, dout):
        re = real_op(x)
        im = imag_op(x)
        re = complex_op(im, re)
        z = reciprocal_op(re)
        zero = zeros_like(dout)
        complex_dout = complex_op(dout, zero)
        return (neg_op(complex_dout * z),)

    return bprop


@bprop_getters.register(P.Erfinv)
def get_bprop_erfinv(self):
    """Grad definition for `Erfinv` operation."""
    exp = P.Exp()
    square = P.Square()
    sqrt = P.Sqrt()
    cast = P.Cast()
    dtype = P.DType()

    def bprop(input_x, out, dout):
        root_pi_over_two = cast(sqrt(F.scalar_to_tensor(np.pi)) / 2, dtype(dout))
        dout_square = square(dout)
        dx = dout * root_pi_over_two * exp(dout_square)
        return (dx,)

    return bprop


@bprop_getters.register(P.BesselI0)
def get_bprop_bessel_i0(self):
    """Generate bprop for BesselI0"""
    bessel_i1 = P.BesselI1()

    def bprop(x, out, dout):
        dx = dout * bessel_i1(x)
        return (dx,)

    return bprop


@bprop_getters.register(P.BesselI1)
def get_bprop_bessel_i1(self):
    """Generate bprop for BesselI1"""
    equal = P.Equal()
    div = P.Div()
    cast = P.Cast()
    dtype = P.DType()
    bessel_i0 = P.BesselI0()

    def bprop(x, out, dout):
        dout_dx = mnp.where(equal(x, 0.), cast(1., dtype(x)), bessel_i0(x) - div(out, x))
        dx = dout * dout_dx
        return (dx,)

    return bprop


@bprop_getters.register(math.BesselJ0)
def get_bprop_bessel_j0(self):
    """Generate bprop for BesselJ0"""
    bessel_j1 = math.BesselJ1()

    def bprop(x, out, dout):
        dx = -dout * bessel_j1(x)
        return (dx,)

    return bprop


@bprop_getters.register(math.BesselJ1)
def get_bprop_bessel_j1(self):
    """Generate bprop for BesselJ1"""
    equal = P.Equal()
    div = P.Div()
    cast = P.Cast()
    dtype = P.DType()
    bessel_j0 = math.BesselJ0()

    def bprop(x, out, dout):
        dout_dx = mnp.where(equal(x, 0.), cast(0.5, dtype(x)), bessel_j0(x) - div(out, x))
        dx = dout * dout_dx
        return (dx,)

    return bprop


@bprop_getters.register(math.BesselK0)
def get_bprop_bessel_k0(self):
    """Generate bprop for BesselK0"""
    bessel_k1 = math.BesselK1()

    def bprop(x, out, dout):
        dx = -dout * bessel_k1(x)
        return (dx,)

    return bprop


@bprop_getters.register(math.BesselK1)
def get_bprop_bessel_k1(self):
    """Generate bprop for BesselK1"""
    div = P.Div()
    bessel_k0 = math.BesselK0()

    def bprop(x, out, dout):
        dout_dx = -(bessel_k0(x) + div(out, x))
        dx = dout * dout_dx
        return (dx,)

    return bprop


@bprop_getters.register(math.BesselK0e)
def get_bprop_bessel_k0e(self):
    """Generate bprop for BesselK0e"""
    bessel_k1e = math.BesselK1e()

    def bprop(x, out, dout):
        dx = dout * (out - bessel_k1e(x))
        return (dx,)

    return bprop


@bprop_getters.register(math.BesselK1e)
def get_bprop_bessel_k1e(self):
    """Generate bprop for BesselK1e"""
    reciprocal = P.Reciprocal()
    bessel_k0e = math.BesselK0e()

    def bprop(x, out, dout):
        dout_dx = out * (1. - reciprocal(x)) - bessel_k0e(x)
        dx = dout * dout_dx
        return (dx,)

    return bprop


@bprop_getters.register(math.BesselY0)
def get_bprop_bessel_y0(self):
    """Generate bprop for BesselY0"""
    bessel_y1 = math.BesselY1()

    def bprop(x, out, dout):
        dx = -dout * bessel_y1(x)
        return (dx,)

    return bprop


@bprop_getters.register(math.BesselY1)
def get_bprop_bessel_y1(self):
    """Generate bprop for BesselY1"""
    div = P.Div()
    bessel_y0 = math.BesselY0()

    def bprop(x, out, dout):
        dout_dx = bessel_y0(x) - div(out, x)
        dx = dout * dout_dx
        return (dx,)

    return bprop


@bprop_getters.register(Hypot)
def get_bprop_hypot(self):
    """Generate bprop for Hypot"""
    mul_ = P.Mul()
    div_ = P.Div()

    def bprop(x1, x2, out, dout):
        x1_f32 = F.cast(x1, mstype.float32)
        x2_f32 = F.cast(x2, mstype.float32)
        out_f32 = F.cast(out, mstype.float32)
        dout_f32 = F.cast(dout, mstype.float32)
        dx1 = mul_(div_(x1_f32, out_f32), dout_f32)
        dx2 = mul_(div_(x2_f32, out_f32), dout_f32)
        result_dx1, result_dx2 = binop_grad_common(x1_f32, x2_f32, dx1, dx2)
        result_dx1 = F.cast(result_dx1, F.dtype(x1))
        result_dx2 = F.cast(result_dx2, F.dtype(x2))
        return (result_dx1, result_dx2)

    return bprop


@bprop_getters.register(P.Asin)
def get_bprop_asin(self):
    """Grad definition for `Asin` operation."""
    input_grad = G.AsinGrad()

    def bprop(input_x, out, dout):
        dx = input_grad(input_x, dout)
        return (dx,)

    return bprop


@bprop_getters.register(P.Trunc)
def get_bprop_trunc(self):
    """Grad definition for `Trunc` operation."""

    def bprop(input_x, output_y, dout):
        bc_x = zeros_like(input_x)
        return (bc_x,)

    return bprop


@bprop_getters.register(P.Ger)
def get_bprop_ger(self):
    """Grad definition for 'Ger' operation"""
    transpose_op = P.Transpose()
    matmul = P.MatMul()
    expand_dims = P.ExpandDims()
    squeeze = P.Squeeze(1)

    def bprop(input_x, input_y, out, dout):
        dx = squeeze(matmul(dout, expand_dims(input_y, 1)))
        dy = squeeze(matmul(transpose_op(dout, (1, 0)), expand_dims(input_x, 1)))
        return dx, dy

    return bprop


@bprop_getters.register(P.Cross)
def get_bprop_cross(self):
    """Grad definition for 'Cross' operation"""
    cross = P.Cross(dim=self.dim)

    def bprop(input1, input2, out, dout):
        return cross(input2, dout), cross(dout, input1)

    return bprop


@bprop_getters.register(P.MulNoNan)
def get_bprop_mul_no_nan(self):
    """Grad definition for `MulNoNan` operation."""
    mul_func = P.Mul()

    def bprop(x, y, out, dout):
        bc_x = mul_func(dout, y)
        bc_y = mul_func(x, dout)
        return binop_grad_common(x, y, bc_x, bc_y)

    return bprop


@bprop_getters.register(Trace)
def get_bprop_trace(self):
    """Grad definition for `Trace` operation."""
    input_grad = G.TraceGrad()
    shape_op = P.Shape()
    to_array = P.TupleToArray()
    cast = P.Cast()

    def bprop(x, out, dout):
        shape = shape_op(x)
        dx = input_grad(dout, cast(to_array(shape), mstype.int64))
        return (dx,)

    return bprop


@bprop_getters.register(G.MinimumGrad)
def get_bprop_minimum_grad(self):
    """Grad definition for 'MinimumGrad' operation"""
    input_grad = G.MinimumGradGrad()

    def bprop(grad, x1, x2, out, dout):
        sopd_x1, sopd_x2, sopd_grads = input_grad(x1, x2, dout[0], dout[1])
        sopd_x1 = 0
        sopd_x2 = 0
        return (sopd_x1, sopd_x2, sopd_grads)

    return bprop


@bprop_getters.register(Bernoulli)
def get_bprop_bernoulli(self):
    """"Grad definition for 'Bernoulli' operation."""

    def bprop(x, p, out, dout):
        return zeros_like(x), zeros_like(p)

    return bprop


@bprop_getters.register(Igamma)
def get_bprop_igamma(self):
    """Grad definition for `Igamma` operation."""
    shape_ = P.Shape()
    igammagrada = G.IgammaGradA()
    lgamma = nn.LGamma()
    log_ = P.Log()
    exp_ = P.Exp()
    reshape_ = P.Reshape()
    reduce_sum_ = P.ReduceSum()

    def bprop(a, x, out, dout):
        sa = shape_(a)
        sx = shape_(x)
        ra, rx = broadcast_gradient_args(sa, sx)
        partial_a = igammagrada(a, x)
        partial_x = exp_(-x + (a - 1) * log_(x) - lgamma(a))
        if ra != () or rx != ():
            return reshape_(reduce_sum_(partial_a * dout, ra), sa), reshape_(reduce_sum_(partial_x * dout, rx), sx)
        return reshape_(partial_a * dout, sa), reshape_(partial_x * dout, sx)

    return bprop


@bprop_getters.register(Igammac)
def get_bprop_igammac(self):
    """Grad definition for `Igammac` operation."""
    shape_ = P.Shape()
    igammagrada = G.IgammaGradA()
    lgamma = nn.LGamma()
    log_ = P.Log()
    exp_ = P.Exp()
    reshape_ = P.Reshape()
    reduce_sum_ = P.ReduceSum()
    neg_ = P.Neg()

    def bprop(a, x, out, dout):
        sa = shape_(a)
        sx = shape_(x)
        ra, rx = broadcast_gradient_args(sa, sx)
        partial_a = igammagrada(a, x)
        partial_x = exp_(-x + (a - 1) * log_(x) - lgamma(a))
        if ra != () or rx != ():
            return neg_(reshape_(reduce_sum_(partial_a * dout, ra), sa)), \
                   neg_(reshape_(reduce_sum_(partial_x * dout, rx), sx))
        return neg_(reshape_(partial_a * dout, sa)), neg_(reshape_(partial_x * dout, sx))

    return bprop


@bprop_getters.register(AddV2)
def get_bprop_add_v2(self):
    """Grad definition for `AddV2` operation."""

    def bprop(x, y, out, dout):
        return binop_grad_common(x, y, dout, dout)

    return bprop


@bprop_getters.register(CholeskySolve)
def get_bprop_cholesky_solve(self):
    """Grad definition for 'CholeskySolve' operation"""
    batchmatmul_op = P.BatchMatMul()
    matmul_op = P.MatMul()
    neg_op = P.Neg()
    shape_op = P.Shape()
    upper = self.upper
    cholesky_solve = CholeskySolve(upper=self.upper)

    def bprop(x1, x2, out, dout):
        flag = 0
        if dout.dtype == mstype.float64:
            flag = 1
            x2 = F.cast(x2, mstype.float32)
            out = F.cast(out, mstype.float32)
            dout = F.cast(dout, mstype.float32)
        dx1 = cholesky_solve(dout, x2)
        if len(shape_op(x2)) == 2:
            common_term = matmul_op(dx1, transpose(out, (1, 0)))
            common_term = common_term + transpose(common_term, (1, 0))
            if upper is True:
                dx2 = neg_op(matmul_op(x2, common_term))
            else:
                dx2 = neg_op(matmul_op(common_term, x2))
        else:
            common_term = batchmatmul_op(dx1, transpose(out, (0, 2, 1)))
            common_term = common_term + transpose(common_term, (0, 2, 1))
            if upper is True:
                dx2 = neg_op(batchmatmul_op(x2, common_term))
            else:
                dx2 = neg_op(batchmatmul_op(common_term, x2))
        if flag == 1:
            dx1 = F.cast(dx1, mstype.float64)
            dx2 = F.cast(dx2, mstype.float64)
        return dx1, dx2

    return bprop
