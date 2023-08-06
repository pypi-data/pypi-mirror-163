# Copyright 2020-2021 Huawei Technologies Co., Ltd
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
"""Class Sensitivity."""

import numpy as np

from mindspore.ops import Stack

from mindspore_xai.explainer import RISE
from mindspore_xai.common.utils import calc_correlation
from .metric import LabelAgnosticMetric


class ClassSensitivity(LabelAgnosticMetric):
    """
    Class sensitivity metric used to evaluate attribution-based explainers.

    Reasonable atrribution-based explainers are expected to generate distinct saliency maps for different labels,
    especially for labels of highest confidence and low confidence. ClassSensitivity evaluates the explainer through
    computing the correlation between saliency maps of highest-confidence and lowest-confidence labels. Explainer with
    better class sensitivity will receive lower correlation score. To make the evaluation results intuitive, the
    returned score will take negative on correlation and normalize.

    Supported Platforms:
        ``Ascend`` ``GPU``
    """

    def evaluate(self, explainer, inputs):
        """
        Evaluate class sensitivity on the explainer.

        Note:
             Currently only single sample (:math:`N=1`) at each call is supported.

        Args:
            explainer (Explainer): The explainer to be evaluated, see `mindspore_xai.explainer`.
            inputs (Tensor): A data sample, a 4D tensor of shape :math:`(N, C, H, W)`.

        Returns:
            numpy.ndarray, 1D array of shape :math:`(N,)`, result of class sensitivity evaluated on `explainer`.

        Raises:
            TypeError: Be raised for any argument type problem.
            ValueError: Be raised if :math:`N` is not 1.

        Examples:
            >>> import numpy as np
            >>> import mindspore as ms
            >>> from mindspore import set_context, PYNATIVE_MODE
            >>> from mindspore_xai.benchmark import ClassSensitivity
            >>> from mindspore_xai.explainer import Gradient
            >>>
            >>> set_context(mode=PYNATIVE_MODE)
            >>> # The detail of LeNet5 is shown in model_zoo.official.cv.lenet.src.lenet.py
            >>> net = LeNet5(10, num_channel=3)
            >>> # prepare your explainer to be evaluated, e.g., Gradient.
            >>> gradient = Gradient(net)
            >>> input_x = ms.Tensor(np.random.rand(1, 3, 32, 32), ms.float32)
            >>> class_sensitivity = ClassSensitivity()
            >>> res = class_sensitivity.evaluate(gradient, input_x)
            >>> print(res.shape)
            (1,)
        """
        self._check_evaluate_param(explainer, inputs)

        outputs = explainer.network(inputs)

        max_confidence_label = outputs.argmax()
        min_confidence_label = outputs.argmin()
        if isinstance(explainer, RISE):
            stack = Stack(axis=1)
            labels = stack([max_confidence_label, min_confidence_label])
            full_saliency = explainer(inputs, labels, show=False)
            max_confidence_saliency = full_saliency[:, max_confidence_label].asnumpy()
            min_confidence_saliency = full_saliency[:, min_confidence_label].asnumpy()
        else:
            max_confidence_saliency = explainer(inputs, max_confidence_label, show=False).asnumpy()
            min_confidence_saliency = explainer(inputs, min_confidence_label, show=False).asnumpy()

        correlations = []
        for i in range(inputs.shape[0]):
            correlation = calc_correlation(max_confidence_saliency[i].reshape(-1),
                                           min_confidence_saliency[i].reshape(-1))
            normalized_correlation = (-correlation + 1) / 2
            correlations.append(normalized_correlation)
        return np.array(correlations, float)
