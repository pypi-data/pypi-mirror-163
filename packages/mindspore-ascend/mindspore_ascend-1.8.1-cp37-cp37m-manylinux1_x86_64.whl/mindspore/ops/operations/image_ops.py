# Copyright 2020-2022 Huawei Technologies Co., Ltd
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

"""image_ops"""
from ... import context
from ..._checkparam import Validator as validator
from ..._checkparam import Rel
from ...common import dtype as mstype
from ..primitive import PrimitiveWithInfer, prim_attr_register, Primitive


class AdjustSaturation(Primitive):
    """
    Adjust saturation of RGB images.

    Note:
        This is a convenience method that converts RGB images to float representation, converts them to HSV,
        adds an offset to the saturation channel, converts back to RGB and then back to the original data type.
        If several adjustments are chained it is advisable to minimize the number of redundant conversions.

    inputs:
        - **image** (Tensor): Images to adjust. Must be one of the following types: float16, float32.
           At least 3-D.The last dimension is interpreted as channels, and must be three.
        - **scale** (Tensor): A float scale to add to the saturation. A Tensor of type float32. Must be 0-D.

    Output:
        Adjusted image(s), same shape and dtype as `image`.

    Raises:
        TypeError: If any iput is not Tensor.
        TypeError: If the type of `image` is not one of the following dtype: float16, float32.
        TypeError: If the type of `scale` is not float32.
        ValueError: If the dimension of the 'image' is less than 3, or the last dimension of the 'image' is not 3.

    Supported Platforms:
        ``Ascend`` ``CPU``

    Examples:
      >>> x = Tensor([[[1.0, 2.0, 3.0],
      ...       [4.0, 5.0, 6.0]],
      ...     [[7.0, 8.0, 9.0],
      ...       [10.0, 11.0, 12.0]]])
      >>> scale = Tensor(float(0.5))
      >>> adjustsaturation = AdjustSaturation()
      >>> output = adjustsaturation(x, scale)
      >>> print(output)
             [[[ 2.         2.4999998  3.       ]
          [ 5.         5.5        6.       ]]
         [[ 8.         8.5        9.       ]
          [11.        11.5       12.       ]]]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize AdjustSaturation"""
        self.init_prim_io_names(inputs=['images', 'scale'], outputs=['y'])


class AdjustContrastv2(Primitive):
    """
    Adjust contrastv2 of images.

    Note:
        images is a tensor of at least 3 dimensions.
        The last 3 dimensions are interpreted as [height, width, channels].
        The other dimensions only represent a collection of images, such as [batch, height, width, channels].
        Contrast is adjusted independently for each channel of each image.

    inputs:
        -**images**(tensor): Images to adjust. Must be one of the following types: float16, float32.
          At least 3-D.The last dimension is interpreted as channels, and must be three.
        -**contrast_factor**(tensor): A float multiplier for adjusting contrast. A Tensor of type float32. Must be 0-D.

    Output:
        Adjusted image(s), same shape and dtype as `images`.

    Raises:
        TypeError: If any input is not Tensor.
        TypeError: If the type of `images` is not one of the following dtype: float16, float32.
        TypeError: If the type of `contrast_factor` is not float32.
        ValueError: If the dimension of the 'images' is less than 3, or the last dimension of the 'images' is not 3.

    Supported Platforms:
        ``Ascend`` ``CPU``

    Examples:
    >>> images = Tensor([[[1.0, 2.0, 3.0],
    ...       [4.0, 5.0, 6.0]],
    ...     [[7.0, 8.0, 9.0],
    ...       [10.0, 11.0, 12.0]]], mstype.float32)
    >>> contrast_factor = Tensor(2., mstype.float32)
    >>> adjustcontrastv2 = AdjustContrastv2()
    >>> output = adjustcontrastv2(images, contrast_factor)
    >>> print(output)
    [[[-3.5 -2.5 -1.5]
      [ 2.5  3.5  4.5]]
    <BLANKLINE>
     [[ 8.5  9.5 10.5]
      [14.5 15.5 16.5]]]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize AdjustContrastv2"""
        self.init_prim_io_names(inputs=['images', 'contrast_factor'], outputs=['y'])


class AdjustHue(Primitive):
    """
    Adjust hue of RGB images.

    Note:
        A convenience method that transform an RGB image to float representation.
        The image is adjusted by transforming the image to HSV and shifting the intensities in the hue channel,
        then transform back to original data mode.
        It is recommended to minimize the number of redundant transformations when several adjustments are chained.

    Inputs:
        - **image** (Tensor): RGB image or images. The size of the last dimension must be 3.
          the dtype is float16 or float32.  At least 3-D.
        - **delta** (Tensor): How much to add to the hue channel, the dtype is float32. Must be 0-D.

    Output:
        Adjusted image(s), same shape and dtype as `image`.

    Raises:
        TypeError: If neither `image` nor `delta` is a tensor.
        TypeError: If the dtype of image not float16 or float32.
        TypeError: If the dtype of delta not float32.
        ValueError: If image have at less than 3 dimensions.

    Supported Platforms:
        ``Ascend`` ``CPU``

    Examples:
         >>> class AdjustHue(nn.Cell):
         ...   def __init__(self):
         ...     super(AdjustHue, self).__init__()
         ...     self.adjustHue = P.AdjustHue()
         ...   def construct(self, image, delta):
         ...     return self.adjustHue(image, delta)
         ...
         >>> image = np.array([[[1, 2, 3], [4, 5, 6]],
         ...                   [[7, 8, 9], [10, 11, 12]],
         ...                   [[13, 14, 15], [16, 17, 18]]]).astype(np.float32)
         >>> delta = 0.2
         >>> adjust_hue = AdjustHue()
         >>> output = adjust_hue(Tensor(image), Tensor(delta))
         >>> print("output", output)
         output [[[ 2.3999996  1.         3.       ]
                  [ 5.3999996  4.         6.       ]]
                 [[ 8.4        7.         9.       ]
                  [11.4       10.        12.       ]]
                 [[14.4       13.        15.       ]
                  [17.4       16.        18.       ]]]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize AdjustHue"""
        self.init_prim_io_names(inputs=['images', 'delta'], outputs=['y'])


class CropAndResize(PrimitiveWithInfer):
    """
    Extracts crops from the input image tensor and resizes them.

    Note:
        In case that the output shape depends on crop_size, the crop_size must be constant.

    Args:
        method (str): An optional string that specifies the sampling method for resizing.
            It can be "bilinear", "nearest" or "bilinear_v2". The option "bilinear" stands for standard bilinear
            interpolation algorithm, while "bilinear_v2" may result in better result in some cases. Default: "bilinear"
        extrapolation_value (float): An optional float value used extrapolation, if applicable. Default: 0.0.

    Inputs:
        - **x** (Tensor) - The input image must be a 4-D tensor of shape [batch, image_height, image_width, depth].
          Types allowed: int8, int16, int32, int64, float16, float32, float64, uint8, uint16.
        - **boxes** (Tensor) - A 2-D tensor of shape [num_boxes, 4].
          The i-th row of the tensor specifies the coordinates of a box in the box_ind[i] image
          and is specified in normalized coordinates [y1, x1, y2, x2]. A normalized coordinate value of y is mapped to
          the image coordinate at y * (image_height - 1), so as the [0, 1] interval of normalized image height is
          mapped to [0, image_height - 1] in image height coordinates. We do allow y1 > y2, in which case the sampled
          crop is an up-down flipped version of the original image. The width dimension is treated similarly.
          Normalized coordinates outside the [0, 1] range are allowed, in which case we use extrapolation_value to
          extrapolate the input image values. Types allowed: float32.
        - **box_index** (Tensor) - A 1-D tensor of shape [num_boxes] with int32 values in [0, batch).
          The value of box_ind[i] specifies the image that the i-th box refers to. Types allowed: int32.
        - **crop_size** (Tuple[int]) - A tuple of two int32 elements: (crop_height, crop_width).
          Only constant value is allowed. All cropped image patches are resized to this size.
          The aspect ratio of the image content is not preserved. Both crop_height and crop_width need to be positive.
    Outputs:
        A 4-D tensor of shape [num_boxes, crop_height, crop_width, depth] with type: float32.

    Raises:
        TypeError: If `method` is not a str.
        TypeError: If `extrapolation_value` is not a float.
        ValueError: If `method` is not one of 'bilinear', 'nearest', 'bilinear_v2'.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> class CropAndResizeNet(nn.Cell):
        ...     def __init__(self, crop_size):
        ...         super(CropAndResizeNet, self).__init__()
        ...         self.crop_and_resize = ops.CropAndResize()
        ...         self.crop_size = crop_size
        ...
        ...     def construct(self, x, boxes, box_index):
        ...         return self.crop_and_resize(x, boxes, box_index, self.crop_size)
        ...
        >>> BATCH_SIZE = 1
        >>> NUM_BOXES = 5
        >>> IMAGE_HEIGHT = 256
        >>> IMAGE_WIDTH = 256
        >>> CHANNELS = 3
        >>> image = np.random.normal(size=[BATCH_SIZE, IMAGE_HEIGHT, IMAGE_WIDTH, CHANNELS]).astype(np.float32)
        >>> boxes = np.random.uniform(size=[NUM_BOXES, 4]).astype(np.float32)
        >>> box_index = np.random.uniform(size=[NUM_BOXES], low=0, high=BATCH_SIZE).astype(np.int32)
        >>> crop_size = (24, 24)
        >>> crop_and_resize = CropAndResizeNet(crop_size=crop_size)
        >>> output = crop_and_resize(Tensor(image), Tensor(boxes), Tensor(box_index))
        >>> print(output.shape)
        (5, 24, 24, 3)
    """

    @prim_attr_register
    def __init__(self, method="bilinear", extrapolation_value=0.0):
        """Initialize CropAndResize"""
        self.init_prim_io_names(inputs=['x', 'boxes', 'box_index', 'crop_size'], outputs=['y'])
        validator.check_value_type("method", method, [str], self.name)
        validator.check_string(method, ["bilinear", "nearest", "bilinear_v2"], "method", self.name)
        self.method = method
        validator.check_value_type("extrapolation_value", extrapolation_value, [float], self.name)
        self.extrapolation_value = extrapolation_value
        self.is_ge = context.get_context("enable_ge")

    def __infer__(self, x, boxes, box_index, crop_size):
        # get shape
        x_shape = list(x['shape'])
        boxes_shape = list(boxes['shape'])
        box_index_shape = list(box_index['shape'])
        # get value
        if crop_size['value'] is None:
            raise ValueError(f"For '{self.name}', the 'crop_size' cannot be None, but got {crop_size['value']}.")
        crop_size_value = crop_size['value']
        # get dtype
        x_dtype = x['dtype']
        boxes_dtype = boxes['dtype']
        box_index_dtype = box_index['dtype']
        crop_size_dtype = crop_size['dtype']
        # check dytpe
        validator.check_tensor_dtype_valid("x", x_dtype,
                                           [mstype.int8, mstype.int16, mstype.int32, mstype.int64, mstype.float16,
                                            mstype.float32, mstype.float64, mstype.uint8, mstype.uint16], self.name)
        validator.check_tensor_dtype_valid("boxes", boxes_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid("box_index", box_index_dtype, [mstype.int32], self.name)
        validator.check_value_type("crop_size", crop_size_value, [tuple], self.name)
        # check input shape rank
        validator.check("x rank", len(x_shape), "expected", 4, Rel.EQ, self.name)
        validator.check("boxes rank", len(boxes_shape), "expected", 2, Rel.EQ, self.name)
        validator.check("box_index rank", len(box_index_shape), "expected", 1, Rel.EQ, self.name)
        validator.check("crop_size size", len(crop_size_value), "expected", 2, Rel.EQ, self.name)
        validator.check("boxes dim_0", boxes_shape[0], "box_index dim_0", box_index_shape[0], Rel.EQ, self.name)
        validator.check("boxes dim_1", boxes_shape[1], "expected", 4, Rel.EQ, self.name)
        # check crop_size_value
        validator.check("crop_height", crop_size_value[0], "minimum", 0, Rel.GT, self.name)
        validator.check("crop_width", crop_size_value[1], "minimum", 0, Rel.GT, self.name)
        # check crop_size element type
        validator.check("crop_height dtype", crop_size_dtype[0], "expected", [mstype.int32, mstype.int64], Rel.IN,
                        self.name)
        validator.check("crop_width dtype", crop_size_dtype[1], "expected", [mstype.int32, mstype.int64], Rel.IN,
                        self.name)

        num_boxes = boxes_shape[0]
        crop_height = crop_size_value[0]
        crop_width = crop_size_value[1]
        depth = x_shape[3]
        out_shape = (num_boxes, crop_height, crop_width, depth)
        if self.is_ge:
            out_shape = (num_boxes, x_shape[1], crop_height, crop_width)
        return {'shape': out_shape,
                'dtype': mstype.float32,
                'value': None}


class NonMaxSuppressionV3(Primitive):
    r"""
        Greedily selects a subset of bounding boxes in descending order of score.

    .. warning::
        When input "max_output_size" is negative, it will be treated as 0.

    Note:
        This algorithm is agnostic to where the origin is in the coordinate system.
        This algorithm is invariant to orthogonal transformations and translations of the coordinate system;
        thus translating or reflections of the coordinate system result in the same boxes being
        selected by the algorithm.

    Inputs:
        - **boxes** (Tensor) - A 2-D Tensor of shape [num_boxes, 4].
        - **scores** (Tensor) - A 1-D Tensor of shape [num_boxes] representing a single score
          corresponding to each box (each row of boxes), the num_boxes of "scores" must be equal to
          the num_boxes of "boxes".
        - **max_output_size** (Union[Tensor, Number.Int]) - A scalar integer Tensor representing the maximum
          number of boxes to be selected by non max suppression.
        - **iou_threshold** (Union[Tensor, Number.Float]) - A 0-D float tensor representing the threshold for
          deciding whether boxes overlap too much with respect to IOU, and iou_threshold must be equal or greater
          than 0 and be equal or smaller than 1.
        - **score_threshold** (Union[Tensor, Number.Float]) - A 0-D float tensor representing the threshold for
          deciding when to remove boxes based on score.

    Outputs:
        A 1-D integer Tensor of shape [M] representing the selected indices from the boxes tensor,
        where M <= max_output_size.

    Raises:
        TypeError: If the dtype of `boxes` and `scores` is different.
        TypeError: If the dtype of `iou_threshold` and `score_threshold` is different.
        TypeError: If `boxes` is not tensor or its dtype is not float16 or float32.
        TypeEroor: If `scores` is not tensor or its dtype is not float16 or float32.
        TypeError: If `max_output_size` is not tensor or scalar.If `max_output_size` is not int32 or int64.
        TypeError: If `iou_threshold` is not tensor or scalar. If its type is not float16 or float32.
        TypeError: If `score_threshold` is not tensor or scalar. If its type is not float16 or float32.
        ValueError: If the size of shape of `boxes` is not 2 or the second value of its shape is not 4.
        ValueError: If the size of shape of `scores` is not 1.
        ValueError: If each of the size of shape of `max_output_size`, `iou_threshold`, `score_threshold` is not 0.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> boxes = Tensor(np.array([[1, 2, 3, 4], [1, 3, 3, 4], [1, 3, 4, 4],
        ...                          [1, 1, 4, 4], [1, 1, 3, 4]]), mstype.float32)
        >>> scores = Tensor(np.array([0.4, 0.5, 0.72, 0.9, 0.45]), mstype.float32)
        >>> max_output_size = Tensor(5, mstype.int32)
        >>> iou_threshold = Tensor(0.5, mstype.float32)
        >>> score_threshold = Tensor(0, mstype.float32)
        >>> nonmaxsuppression = ops.NonMaxSuppressionV3()
        >>> output = nonmaxsuppression(boxes, scores, max_output_size, iou_threshold, score_threshold)
        >>> print(output)
        [3 2 0]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize NonMaxSuppressionV3"""


class NonMaxSuppressionWithOverlaps(Primitive):
    """
    Greedily selects a subset of bounding boxes in descending order of score.

    Note:
        This algorithm is agnostic to where the origin is in the coordinate system.
        This algorithm is invariant to orthogonal transformations and translations of the coordinate system;
        thus translating or reflections of the coordinate system result in the same boxes being
        selected by the algorithm.

    Inputs:
        - **overlaps** (Tensor) - A 2-D Tensor of shape [num_boxes, num_boxes].
          Types allowed:float32.
        - **scores** (Tensor) - A 1-D Tensor of shape [num_boxes] representing a single score
          corresponding to each box (each row of boxes),the num_boxes of "scores" must be equal to
          the num_boxes of "overlaps".
          Types allowed:float32.
        - **max_output_size** (Tensor) - A scalar integer Tensor representing the maximum
          number of boxes to be selected by non max suppression, and max_output_size must be equal to or greater
          than 0.
          Types allowed:int32.
        - **overlap_threshold** (Tensor) - A 0-D float tensor representing the threshold for deciding
          whether boxes overlap too much.
          Types allowed:float32.
        - **score_threshold** (Tensor) - A 0-D float tensor representing the threshold for
          deciding when to remove boxes based on score.
          Types allowed:float32.

    Outputs:
        An int32 tensor. A 1-D integer Tensor of shape [M] representing the selected indices from the boxes tensor,
        where M <= max_output_size.

    Raises:
        TypeError: If the dtype of `overlaps` and `scores` is not float32.
        TypeError: If the dtype of `overlap_threshold` and `score_threshold` is not float32.
        TypeError: If `overlaps` is not tensor or its dtype is not float32.
        TypeError: If `scores` is not tensor or its dtype is not float32.
        TypeError: If `max_output_size` is not tensor or scalar.If `max_output_size` is not int32.
        TypeError: If `overlap_threshold` is not tensor or scalar. If its type is not float32.
        TypeError: If `score_threshold` is not tensor or scalar. If its type is not float32.
        ValueError: If the size of shape of `overlaps` is not 2 or the second value of its shape
                    is not equal to the first value of its shape.
        ValueError: If the size of shape of `scores` is not 1.
        ValueError: If each of the size of shape of `max_output_size`, `overlap_threshold`, `score_threshold` is not 0.
        ValueError: If `max_output_size` is negative.
        ValueError: If the shape of `scores` is not equal to the shape of the dim0 or dim1 of `overlaps`.

    Supported Platforms:
        ``Ascend`` ``CPU``

    Examples:
        >>> overlaps = Tensor(np.array([[0.6964692, 0.28613934, 0.22685145, 0.5513148],
                                [0.71946895, 0.42310646, 0.9807642, 0.6848297],
                                [0.4809319, 0.39211753, 0.343178, 0.7290497],
                                [0.43857226, 0.059677895, 0.39804426, 0.7379954]
                                ]), mstype.float32)
        >>> scores = Tensor(np.array([0.18249173, 0.17545176, 0.53155136, 0.53182757]), mstype.float32)
        >>> max_output_size = Tensor(4, mstype.int32)
        >>> overlap_threshold = Tensor(0.1, mstype.float32)
        >>> score_threshold = Tensor(0.2, mstype.float32)
        >>> nonmaxsuppression = ops.NonMaxSuppressionWithOverlaps()
        >>> output = nonmaxsuppression(overlaps, scores, max_output_size, overlap_threshold, score_threshold)
        >>> print(output)
        [3]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize NonMaxSuppressionWithOverlaps"""


class HSVToRGB(Primitive):
    """
    Convert one or more images from HSV to RGB. The format of the image(s) should be NHWC.

    Inputs:
        - **x** (Tensor) - The input image must be a 4-D tensor of shape [batch, image_height, image_width, channel].
          Number of channel must be 3.
          Types allowed: float16, float32, float64.
    Outputs:
        A 4-D tensor of shape [batch, image_height, image_width, channel] with same type of input.

    Raises:
        TypeError: If `x` is not a Tensor.
        TypeError: If the dtype of `x` is not float16, float32, float64.
        ValueError: If rank of the `x` is not equal to 4.
        ValueError: If the last dimension of `x` is not equal to 3.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> image = np.array([0.5, 0.5, 0.5]).astype(np.float32).reshape([1, 1, 1, 3])
        >>> hsv_to_rgb = P.HSVToRGB()
        >>> output = hsv_to_rgb(Tensor(image))
        >>> print(output)
        [[[[0.25 0.5  0.5 ]]]]
    """
    @prim_attr_register
    def __init__(self):
        pass


class CropAndResizeGradBoxes(Primitive):
    """
    Computes the gradient of the CropAndResize op with respect to the input boxes tensor.

    Note:
        Input images and grads must be a 4-D tensor.

    Args:
        method (str): A string specifying the interpolation method. Only "bilinear" is supported for now.
            Default: "bilinear".

    Inputs:
        - **grads** (Tensor) - A 4-D tensor of shape [num_boxes, crop_height, crop_width, depth].
          The format must be NHWC. Types allowed: float32.
        - **images** (Tensor) - A 4-D tensor of shape [batch, image_height, image_width, depth].
          The format must be NHWC. Types allowed: int8, int16, int32, int64, float16, float32, float64, uint8, uint16.
          Both image_height and image_width need to be positive.
        - **boxes** (Tensor) - A 2-D tensor of shape [num_boxes, 4].
          The i-th row of the tensor specifies the coordinates of a box in the box_index[i] image
          and is specified in normalized coordinates [y1, x1, y2, x2]. A normalized coordinate value of y is mapped to
          the image coordinate at y * (image_height - 1), so as the [0, 1] interval of normalized image height is
          mapped to [0, image_height - 1] in image height coordinates. We do allow y1 > y2, in which case the sampled
          crop is an up-down flipped version of the original image. The width dimension is treated similarly.
          Normalized coordinates outside the [0, 1] range are allowed, in which case we use extrapolation_value to
          extrapolate the input image values. Types allowed: float32.
        - **box_index** (Tensor) - A 1-D tensor of shape [num_boxes] with int32 values in [0, batch).
          The value of box_index[i] specifies the image that the i-th box refers to. Types allowed: int32.

    Outputs:
        A 2-D tensor of shape [num_boxes, 4] with type: float32.

    Raises:
        TypeError: If `method` is not a str.
        TypeError: If `grads` is not tensor or its dtype is not float32.
        TypeError: If `images` is not tensor or its dtype is incorrect.
        TypeError: If `boxes` is not tensor or its dtype is not float32.
        TypeError: If `box_index` is not tensor or its dtype is not int32.
        ValueError: If `method` is not 'bilinear'.
        ValueError: If the size of `grads` tensor shape is not equal to 4.
        ValueError: If the size of `images` tensor shape is not equal to 4.
        ValueError: If the value of image_height or image_width of `image` tensor shape is not positive.
        ValueError: If the size of `boxes` tensor shape is not equal to 2.
        ValueError: If the length of the second dimension of `boxes` is not equal to 4.
        ValueError: If the size of `box_index` tensor shape is not equal to 1.
        ValueError: If the length of `box_index` is not equal to num_boxes.

    Supported Platforms:
        ``Ascend`` ``CPU``

    Examples:
        >>> crop_and_resize_grad_boxes = ops.CropAndResizeGradBoxes(method = "bilinear")
        >>> grads = Tensor(np.array([[[[2.0], [5.0]], [[1.0], [4.0]]]]), mindspore.float32)
        >>> image = Tensor(np.array([[[[9.0], [5.0], [2.0], [1.0]],
        ...                           [[6.0], [1.0], [9.0], [7.0]],
        ...                           [[6.0], [0.0], [2.0], [9.0]],
        ...                           [[1.0], [2.0], [6.0], [7.0]]]]), mindspore.float32)
        >>> boxes = Tensor(np.array([[0.3, 0.8, 0.3, 0.8]]), mindspore.float32)
        >>> box_index = Tensor(np.array([0]), mindspore.int32)
        >>> output = crop_and_resize_grad_boxes(grads, image, boxes, box_index)
        >>> print(output.asnumpy())
        [138.6,-17.1,99.0,-51.300003]
    """

    @prim_attr_register
    def __init__(self, method="bilinear"):
        """Initialize CropAndResizeGradBoxes"""
        self.init_prim_io_names(inputs=['grads', 'images', 'boxes', 'box_index'], outputs=['y'])
        validator.check_value_type("method", method, [str], self.name)
        validator.check_string(method, ["bilinear"], "method", self.name)
        self.method = method


class ResizeLinear1D(Primitive):
    r"""
    Using the linear interpolate method resize the input tensor 'x'.

    For general resize, refer to :func:`mindspore.ops.interpolate` for more detail.

    .. warning::
        This is an experimental feature and is subjected to change.

    Args:
        coordinate_transformation_mode (string): Default is 'align_corners'. Describes how to transform the coordinate
            in the resized tensor to the coordinate in the original tensor. Other optional: 'half_pixel', 'asymmetric'.

    Inputs:
        - **x** (Tensor) - A 3-D tensor which to resize, with shape [batch, channel, width]. Must be one of the
            following types: uint8, int8, int16, int32, int64, float16, float32, double.
        - **size** (Tensor) - A 1-D int64 Tensor, describes the size of the output tensor.

    Outputs:
        A 3-D tensor which shape is [batch, channel, new_width] with the same type as `x`.

    Raises:
        TypeError: If dtype of `x` is not in the support list.
        TypeError: If `size` is not a 1-D int64_t tensor.
        TypeError: If `coordinate_transformation_mode` is not a string.
        TypeError: If `coordinate_transformation_mode` is not in the support list.

    Supported Platforms:
        ``CPU`` ``GPU``

    Examples:
        >>> input = Tensor([[[1, 2, 3], [4, 5, 6]]], mindspore.float32)
        >>> size = Tensor([6], mindspore.int32)
        >>> resize_linear_1d = ops.ResizeLinear1D(coordinate_transformation_mode="align_corners")
        >>> output = resize_linear_1d(x=input, size=size)
        >>> print(output)
        [[[1. 1.4 1.8 2.2 2.6 3.]
          [4. 4.4 4.8 5.2 5.6 6.]]]
    """

    @prim_attr_register
    def __init__(self, coordinate_transformation_mode="align_corners"):
        """Initialize ResizeLinear1D."""
        self.init_prim_io_names(inputs=["x", "sizes"], outputs=["output"])
        validator.check_value_type(
            "coordinate_transformation_mode", coordinate_transformation_mode, [str], self.name)
        validator.check_string(coordinate_transformation_mode, ["align_corners", "half_pixel", "asymmetric"],
                               "coordinate_transformation_mode", self.name)


class ResizeBilinearV2(Primitive):
    r"""
    Resizes an image to a certain size using the bilinear interpolation.

    The resizing only affects the lower two dimensions which represent the height and width.

    Args:
        align_corners (bool): If true, rescale input by :math:`(new\_height - 1) / (height - 1)`,
                       which exactly aligns the 4 corners of images and resized images. If false,
                       rescale by :math:`new\_height / height`. Default: False.
        half_pixel_centers (bool): Whether half pixel center. If set to True, `align_corners` should be False.
                           Default: False.

    Inputs:
        - **x** (Tensor): Image to be resized. Input images must be a 4-D tensor with shape
            :math:`(batch, channels, height, width)`, with data type of float32 or float16.
        - **size** (Union[tuple[int], list[int], Tensor]): The new size of the images.
            A tuple or list or Tensor of 2 int elements :math:`(new\_height, new\_width)`.

    Outputs:
        Tensor, resized image. 4-D with shape :math:`(batch, channels, new\_height, new\_width)`,
        with the same data type as input `x`.

    Raises:
        TypeError: If `align_corners` is not a bool.
        TypeError: If `half_pixel_centers` is not a bool.
        TypeError: If `align_corners` and `half_pixel_centers` are all True.
        ValueError: If `half_pixel_centers` is True and device_target is CPU.

    Supported Platforms:
        ``Ascend`` ``CPU`` ``GPU``

    Examples:
        >>> x = Tensor([[[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]]], mindspore.float32)
        >>> output = ResizeBilinearV2(x, (5, 5))
        >>> print(output)
        [[[[1. 2. 3. 4. 5.]
           [1. 2. 3. 4. 5.]
           [1. 2. 3. 4. 5.]
           [1. 2. 3. 4. 5.]
           [1. 2. 3. 4. 5.]]]]
    """

    @prim_attr_register
    def __init__(self, align_corners=False, half_pixel_centers=False):
        """Initialize ResizeBilinear."""
        super().__init__(name="ResizeBilinearV2")
        self.init_prim_io_names(inputs=['x', 'size'], outputs=['y'])
        self.align_corners = validator.check_value_type("align_corners", align_corners, [bool], self.name)
        self.half_pixel_centers = validator.check_value_type("half_pixel_centers",
                                                             half_pixel_centers, [bool], self.name)
        if half_pixel_centers and align_corners:
            raise ValueError(f"If half_pixel_centers is True, align_corners must be False, but got {align_corners}")
        target = context.get_context("device_target")
        if half_pixel_centers and target == "CPU":
            raise ValueError(f"Currently `half_pixel_centers`=True is not supported in CPU device_target")
