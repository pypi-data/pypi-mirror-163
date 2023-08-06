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


"""Define the grad rules of neural network related operations."""
from mindspore import Tensor
from mindspore.ops.operations.nn_ops import GridSampler2D
from mindspore.ops.operations.nn_ops import GridSampler3D
from mindspore.ops.primitive import constexpr
from mindspore.common import dtype as mstype
from .._grad.grad_base import bprop_getters
from .. import operations as P
from ..composite.multitype_ops.zeros_like_impl import zeros_like
from ..operations import _grad_ops as G
from ..operations.nn_ops import FractionalMaxPool
from ..operations._grad_ops import FractionalMaxPoolGrad
from ..operations.nn_ops import FractionalMaxPool3DWithFixedKsize
from ..operations._grad_ops import FractionalMaxPool3DGradWithFixedKsize
from ..operations.nn_ops import FractionalAvgPool
from ..operations._grad_ops import FractionalAvgPoolGrad
from ..operations.nn_ops import NthElement
from ..operations.nn_ops import PSROIPooling
from ..operations._grad_ops import PSROIPoolingGrad
from ..operations.nn_ops import AvgPoolV1
from ..operations._grad_ops import AvgPoolGradV1
from ..operations.nn_ops import MaxPoolV1
from ..operations._grad_ops import MaxPoolGradV1
from ..operations.nn_ops import ReLUV3
from ..operations._grad_ops import ReluGrad
from ..operations.image_ops import ResizeLinear1D
from ..operations.nn_ops import MaxPool3DWithArgmax


@bprop_getters.register(P.CTCLossV2)
def get_bprop_ctc_loss_v2(self):
    """Grad definition for `CTCLossV2` operation"""
    ctc_loss_grad = P.CTCLossV2Grad(self.blank, self.reduction, self.zero_infinity)

    def bprop(log_probs, targets, input_lengths, target_lengths, out, dout):
        grad = ctc_loss_grad(dout[0], log_probs, targets, input_lengths, target_lengths, out[0], out[1])
        return grad, zeros_like(targets), zeros_like(input_lengths), zeros_like(target_lengths)

    return bprop


@bprop_getters.register(P.SoftMarginLoss)
def get_bprop_soft_margin_loss(self):
    """Grad definition for `SoftMarginLoss` operation."""
    grad = G.SoftMarginLossGrad(reduction=self.reduction)

    def bprop(predict, label, out, dout):
        dx = grad(predict, label, dout)
        dy = grad(label, predict, dout)
        return dx, dy

    return bprop


@bprop_getters.register(P.SoftShrink)
def get_bprop_softshrink(self):
    """Grad definition for `SoftShrink` operation."""
    input_grad = G.SoftShrinkGrad(self.lambd)

    def bprop(input_x, out, dout):
        dx = input_grad(dout, input_x)
        return (dx,)

    return bprop


@bprop_getters.register(P.HShrink)
def get_bprop_hshrink(self):
    """Grad definition for `HShrinkGrad` operation."""
    grad = G.HShrinkGrad(self.lambd)

    def bprop(features, out, gradients):
        dx = grad(gradients, features)
        return (dx,)

    return bprop


@bprop_getters.register(P.CeLU)
def get_bprop_celu(self):
    """Grad definition for `CeLU` operation."""
    alpha = self.alpha
    greater_equal = P.GreaterEqual()
    less = P.Less()

    def bprop(x, out, dout):
        greater = greater_equal(x, 0.0)
        lesser = less(x, 0.0)
        dx = dout * (greater * 1.0 + lesser * (out / alpha + 1.0))
        return (dx,)

    return bprop


@bprop_getters.register(GridSampler3D)
def get_bprop_grid_sampler_3d(self):
    """Grad definition for `GridSampler3D` operation."""
    grad = G.GridSampler3DGrad(self.interpolation_mode, self.padding_mode, self.align_corners)

    def bprop(input_x, grid, out, dout):
        dx, dgrid = grad(dout, input_x, grid)
        return dx, dgrid
    return bprop


@bprop_getters.register(ReLUV3)
def get_bprop_relu(self):
    """Grad definition for `ReLUV3` operation."""
    input_grad = ReluGrad()

    def bprop(x, out, dout):
        dx = input_grad(dout, out)
        return (dx,)

    return bprop


@bprop_getters.register(NthElement)
def get_bprop_nth_element(self):
    """Grad definition for `NthElement` operation."""
    expand_dims = P.ExpandDims()
    cast = P.Cast()
    equal = P.Equal()
    reduce_sum = P.ReduceSum()
    divide = P.Div()
    def bprop(input_x, n, out, dout):
        indicators = cast(equal(expand_dims(out, -1), input_x), input_x.dtype)
        dout = expand_dims(dout, -1)
        num_select = expand_dims(reduce_sum(indicators, -1), -1)
        return divide(indicators, num_select) * dout, None

    return bprop


@bprop_getters.register(FractionalMaxPool)
def get_bprop_fractional_max_pool(self):
    """Grad definition for `FractionalMaxPool` operation."""
    fractional_max_pool_grad = FractionalMaxPoolGrad(self.overlapping)

    def bprop(x, out, dout):
        dx = fractional_max_pool_grad(x, out[0], dout[0], out[1], out[2])
        return (dx,)

    return bprop


@bprop_getters.register(FractionalMaxPool3DWithFixedKsize)
def get_bprop_fractional_max_pool3d_with_fixed_ksize(self):
    """Grad definition for `FractionalMaxPool3DWithFixedKsize` operation."""
    fractional_max_pool3d_grad_with_fixed_ksize = FractionalMaxPool3DGradWithFixedKsize(data_format=self.data_format)

    def bprop(x, random_samples, out, dout):
        dx = fractional_max_pool3d_grad_with_fixed_ksize(x, dout[0], out[1])
        return (dx, zeros_like(random_samples))

    return bprop


@constexpr
def _create_tensor(x_shape):
    return Tensor(x_shape, mstype.int64)


@bprop_getters.register(FractionalAvgPool)
def get_bprop_fractional_avg_pool(self):
    """Grad definition for `FractionalAvgPool` operation."""
    fractional_avg_pool_grad = FractionalAvgPoolGrad(overlapping=self.overlapping)

    def bprop(x, out, dout):
        dx = fractional_avg_pool_grad(_create_tensor(x.shape), dout[0], out[1], out[2])
        return (dx,)

    return bprop


@bprop_getters.register(PSROIPooling)
def get_bprop_p_s_r_o_i_pooling(self):
    """Grad definition for `PSROIPooling` operation."""
    spatial_scale = self.spatial_scale
    group_size = self.group_size
    output_dim = self.output_dim

    def bprop(x, rois, out, dout):
        shape = P.Shape()(x)
        p_s_r_o_i_pooling_grad = PSROIPoolingGrad((shape[2:]), spatial_scale, group_size, output_dim)
        dx = p_s_r_o_i_pooling_grad(dout, rois)
        return (dx, zeros_like(rois))

    return bprop


@bprop_getters.register(AvgPoolV1)
def get_bprop_avg_pool_v1_grad(self):
    """Grad definition for `AvgPoolV1` operation."""
    avgpool_grad_v1 = AvgPoolGradV1(
        kernel_size=self.kernel_size,
        strides=self.strides,
        pad_mode=self.pad_mode,
        data_format=self.format)
    to_arr = P.TupleToArray()
    get_shape = P.Shape()

    def bprop(x, out, dout):
        orig_input_shape = to_arr(get_shape(x))
        dx = avgpool_grad_v1(orig_input_shape, dout)
        return (dx,)

    return bprop


@bprop_getters.register(MaxPoolV1)
def get_bprop_max_pool_v1_grad(self):
    """Grad definition for `MaxPoolV1` operation."""
    maxpool_grad_v1 = MaxPoolGradV1(
        kernel_size=self.kernel_size,
        strides=self.strides,
        pad_mode=self.pad_mode,
        data_format=self.format)

    def bprop(x, out, dout):
        dx = maxpool_grad_v1(x, out, dout)
        return (dx,)
    return bprop


@bprop_getters.register(GridSampler2D)
def get_bprop_grid_sampler_2d(self):
    """Grad definition for `GridSampler2D` operation."""
    grad = G.GridSampler2DGrad(self.interpolation_mode, self.padding_mode, self.align_corners)

    def bprop(input_x, grid, out, dout):
        dx, dgrid = grad(dout, input_x, grid)
        return dx, dgrid

    return bprop


@bprop_getters.register(ResizeLinear1D)
def get_bprop_resize_bilinear(self):
    """Grad definition for `ResizeLinear1D` operation."""
    resize_grad = G.ResizeLinear1DGrad(self.coordinate_transformation_mode)

    def bprop(input_x, size, out, dout):
        dx = resize_grad(dout, input_x)
        return (dx, zeros_like(size))

    return bprop


@bprop_getters.register(MaxPool3DWithArgmax)
def get_bprop_maxpool3dwithargmax(self):
    """Grad definition for `MaxPool3DWithArgmax` operation."""
    maxpool3dwithargmax_grad = G.MaxPool3DGradWithArgmax(
        ksize=self.ksize,
        strides=self.strides,
        pads=self.pads,
        dilation=self.dilation,
        ceil_mode=self.ceil_mode,
        data_format=self.data_format)

    def bprop(x, out, dout):
        dx = maxpool3dwithargmax_grad(x, dout[0], out[1])
        return (dx,)

    return bprop
