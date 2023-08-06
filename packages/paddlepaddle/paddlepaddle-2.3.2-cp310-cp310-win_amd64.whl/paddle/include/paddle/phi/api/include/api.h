#pragma once

#include <tuple>

#include "paddle/phi/api/include/tensor.h"
#include "paddle/phi/common/scalar.h"
#include "paddle/phi/common/int_array.h"
#include "paddle/utils/optional.h"

namespace paddle {
namespace experimental {


PADDLE_API Tensor abs(const Tensor& x);

PADDLE_API std::tuple<Tensor,Tensor,Tensor> accuracy(const Tensor& x, const Tensor& indices, const Tensor& label);

PADDLE_API Tensor acos(const Tensor& x);

PADDLE_API Tensor acosh(const Tensor& x);

PADDLE_API std::tuple<Tensor,Tensor,Tensor> adadelta(const Tensor& param, const Tensor& grad, const Tensor& avg_squared_grad, const Tensor& avg_squared_update, float rho, float epsilon);

PADDLE_API std::tuple<Tensor,Tensor,Tensor> adamax(const Tensor& param, const Tensor& grad, const Tensor& learning_rate, const Tensor& moment, const Tensor& inf_norm, const Tensor& beta1_pow, float beta1, float beta2, float epsilon);

PADDLE_API Tensor add(const Tensor& x, const Tensor& y);

PADDLE_API Tensor add_n(const std::vector<Tensor>& x);

PADDLE_API Tensor addmm(const Tensor& input, const Tensor& x, const Tensor& y, float alpha, float beta);

PADDLE_API Tensor all(const Tensor& x, const std::vector<int64_t>& dims={}, bool keep_dim=false);

PADDLE_API Tensor allclose(const Tensor& x, const Tensor& y, const Scalar& rtol, const Scalar& atol, bool equal_nan);

PADDLE_API Tensor any(const Tensor& x, const std::vector<int64_t>& dims={}, bool keep_dim=false);

PADDLE_API Tensor arange(const Tensor& start, const Tensor& end, const Tensor& step, DataType dtype, const Place& place={});

PADDLE_API Tensor argmax(const Tensor& x, int64_t axis, bool keepdims, bool flatten, int dtype);

PADDLE_API Tensor argmin(const Tensor& x, int64_t axis, bool keepdims, bool flatten, int dtype);

PADDLE_API std::tuple<Tensor,Tensor> argsort(const Tensor& x, int axis, bool descending);

PADDLE_API Tensor asin(const Tensor& x);

PADDLE_API Tensor asinh(const Tensor& x);

PADDLE_API Tensor assign(const Tensor& x);

PADDLE_API Tensor atan(const Tensor& x);

PADDLE_API Tensor atan2(const Tensor& x, const Tensor& y);

PADDLE_API Tensor atanh(const Tensor& x);

PADDLE_API std::tuple<Tensor,Tensor,Tensor> auc(const Tensor& x, const Tensor& label, const Tensor& stat_pos, const Tensor& stat_neg, const std::string& curve, int num_thresholds, int slide_steps);

PADDLE_API std::tuple<Tensor,Tensor,Tensor,Tensor,Tensor,Tensor> batch_norm(const Tensor& x, const Tensor& scale, const Tensor& bias, const Tensor& mean, const Tensor& variance, float momentum, float epsilon, const std::string& data_layout, bool is_test, bool use_global_stats, bool trainable_statistics, bool fuse_with_relu);

PADDLE_API Tensor bce_loss(const Tensor& input, const Tensor& label);

PADDLE_API Tensor bernoulli(const Tensor& x);

PADDLE_API Tensor bitwise_and(const Tensor& x, const Tensor& y);

PADDLE_API Tensor bitwise_not(const Tensor& x);

PADDLE_API Tensor bitwise_or(const Tensor& x, const Tensor& y);

PADDLE_API Tensor bitwise_xor(const Tensor& x, const Tensor& y);

PADDLE_API Tensor brelu(const Tensor& x, float t_min, float t_max);

PADDLE_API Tensor cast(const Tensor& x, DataType out_dtype);

PADDLE_API Tensor ceil(const Tensor& x);

PADDLE_API Tensor cholesky(const Tensor& x, bool upper);

PADDLE_API Tensor cholesky_solve(const Tensor& x, const Tensor& y, bool upper);

PADDLE_API Tensor clip(const Tensor& x, const Scalar& min, const Scalar& max);

PADDLE_API Tensor clip_(const Tensor& x, const Scalar& min, const Scalar& max);

PADDLE_API Tensor concat(const std::vector<Tensor>& x, const Scalar& axis);

PADDLE_API Tensor conj(const Tensor& x);

PADDLE_API Tensor conv2d(const Tensor& input, const Tensor& filter, const std::vector<int>& strides, const std::vector<int>& paddings, const std::string& paddding_algorithm, int groups, const std::vector<int>& dilations, const std::string& data_format, bool use_addto, int workspace_size_MB, bool exhaustive_search);

PADDLE_API Tensor conv2d_transpose(const Tensor& x, const Tensor& filter, const std::vector<int>& strides, const std::vector<int>& paddings, const std::vector<int>& output_padding, const std::vector<int>& output_size, const std::string& padding_algorithm, int groups, const std::vector<int>& dilations, const std::string& data_format);

PADDLE_API Tensor conv3d_transpose(const Tensor& x, const Tensor& filter, const std::vector<int>& strides, const std::vector<int>& paddings, const std::vector<int>& output_padding, const std::vector<int>& output_size, const std::string& padding_algorithm, int groups, const std::vector<int>& dilations, const std::string& data_format);

PADDLE_API Tensor copy_to(const Tensor& x, const Place& place, bool blocking);

PADDLE_API Tensor cos(const Tensor& x);

PADDLE_API Tensor cosh(const Tensor& x);

PADDLE_API Tensor cross(const Tensor& x, const Tensor& y, int axis=9);

PADDLE_API std::tuple<Tensor,Tensor> cross_entropy_with_softmax(const Tensor& input, const Tensor& label, bool soft_label, bool use_softmax, bool numeric_stable_mode, int ignore_index, int axis);

PADDLE_API Tensor cumprod(const Tensor& x, int dim);

PADDLE_API Tensor cumsum(const Tensor& x, int axis, bool flatten, bool exclusive, bool reverse);

PADDLE_API Tensor deformable_conv(const Tensor& x, const Tensor& offset, const Tensor& filter, paddle::optional<const Tensor&> mask, const std::vector<int>& strides, const std::vector<int>& paddings, const std::vector<int>& dilations, int deformable_groups, int groups, int im2col_step);

PADDLE_API Tensor depthwise_conv2d_transpose(const Tensor& x, const Tensor& filter, const std::vector<int>& strides, const std::vector<int>& paddings, const std::vector<int>& output_padding, const std::vector<int>& output_size, const std::string& padding_algorithm, int groups, const std::vector<int>& dilations, const std::string& data_format);

PADDLE_API Tensor det(const Tensor& x);

PADDLE_API Tensor diag(const Tensor& x, int offset, float padding_value);

PADDLE_API Tensor diagonal(const Tensor& x, int offset, int axis1, int axis2);

PADDLE_API Tensor digamma(const Tensor& x);

PADDLE_API Tensor dist(const Tensor& x, const Tensor& y, float p);

PADDLE_API Tensor divide(const Tensor& x, const Tensor& y);

PADDLE_API Tensor dot(const Tensor& x, const Tensor& y);

PADDLE_API std::tuple<Tensor,Tensor> dropout(const Tensor& x, paddle::optional<const Tensor&> seed_tensor, float p, bool is_test, const std::string& mode, int seed, bool fix_seed);

PADDLE_API std::tuple<Tensor,Tensor> eigh(const Tensor& x, const std::string& uplo);

PADDLE_API std::tuple<Tensor,std::vector<Tensor>,std::vector<Tensor>> einsum(const std::vector<Tensor>& x, const std::string& equation);

PADDLE_API Tensor elementwise_pow(const Tensor& x, const Tensor& y);

PADDLE_API Tensor elu(const Tensor& x, float alpha);

PADDLE_API Tensor empty(const IntArray& shape, DataType dtype=DataType::FLOAT32, const Place& place=CPUPlace());

PADDLE_API Tensor empty_like(const Tensor& x, DataType dtype=DataType::UNDEFINED, const Place& place={});

PADDLE_API Tensor equal(const Tensor& x, const Tensor& y, int axis=-1);

PADDLE_API Tensor equal_all(const Tensor& x, const Tensor& y);

PADDLE_API Tensor erf(const Tensor& x);

PADDLE_API Tensor erfinv(const Tensor& x);

PADDLE_API Tensor exp(const Tensor& x);

PADDLE_API Tensor expand(const Tensor& x, const IntArray& shape);

PADDLE_API Tensor expand_as(const Tensor& x, paddle::optional<const Tensor&> y, const std::vector<int>& target_shape);

PADDLE_API Tensor expm1(const Tensor& x);

PADDLE_API Tensor eye(int64_t num_rows, int64_t num_columns, DataType dtype=DataType::FLOAT32, const Place& place={});

PADDLE_API std::tuple<Tensor,Tensor> flatten(const Tensor& x, int start_axis, int stop_axis);

PADDLE_API std::tuple<Tensor,Tensor> flatten_(const Tensor& x, int start_axis, int stop_axis);

PADDLE_API Tensor flip(const Tensor& x, const std::vector<int>& axis);

PADDLE_API Tensor floor(const Tensor& x);

PADDLE_API Tensor floor_divide(const Tensor& x, const Tensor& y);

PADDLE_API Tensor fmax(const Tensor& x, const Tensor& y, int axis);

PADDLE_API Tensor fmin(const Tensor& x, const Tensor& y, int axis);

PADDLE_API Tensor frobenius_norm(const Tensor& x, const std::vector<int64_t>& axis, bool keep_dim, bool reduce_all);

PADDLE_API Tensor full(const IntArray& shape, const Scalar& value, DataType dtype=DataType::FLOAT32, const Place& place=CPUPlace());

PADDLE_API Tensor full_batch_size_like(const Tensor& input, const std::vector<int>& shape, DataType dtype, const Scalar& value, int input_dim_idx, int output_dim_idx, const Place& place=CPUPlace());

PADDLE_API Tensor full_like(const Tensor& x, const Scalar& value, DataType dtype=DataType::UNDEFINED, const Place& place={});

PADDLE_API Tensor gather(const Tensor& x, const Tensor& index, const Scalar& axis=0);

PADDLE_API Tensor gather_nd(const Tensor& x, const Tensor& index);

PADDLE_API Tensor gather_tree(const Tensor& ids, const Tensor& parents);

PADDLE_API Tensor gaussian_random(const IntArray& shape, float mean, float std, int seed, DataType dtype, const Place& place={});

PADDLE_API Tensor gelu(const Tensor& x, bool approximate);

PADDLE_API Tensor graph_send_recv(const Tensor& x, const Tensor& src_index, const Tensor& dst_index, const std::string& pool_type="SUM", int64_t out_size=0);

PADDLE_API Tensor greater_equal(const Tensor& x, const Tensor& y, int axis=-1);

PADDLE_API Tensor greater_than(const Tensor& x, const Tensor& y, int axis=-1);

PADDLE_API Tensor gumbel_softmax(const Tensor& x, float temperature, bool hard, int axis);

PADDLE_API Tensor hard_shrink(const Tensor& x, float threshold);

PADDLE_API Tensor hard_sigmoid(const Tensor& x, float slope, float offset);

PADDLE_API Tensor hard_swish(const Tensor& x, float threshold=6.0, float scale=6.0, float offset=3.0);

PADDLE_API Tensor histogram(const Tensor& x, int64_t bins, int min, int max);

PADDLE_API std::tuple<Tensor,Tensor> huber_loss(const Tensor& input, const Tensor& label, float delta);

PADDLE_API Tensor imag(const Tensor& x);

PADDLE_API Tensor increment(const Tensor& x, float value);

PADDLE_API Tensor index_sample(const Tensor& x, const Tensor& index);

PADDLE_API Tensor index_select(const Tensor& x, const Tensor& index, int dim);

PADDLE_API Tensor is_empty(const Tensor& x);

PADDLE_API Tensor isclose(const Tensor& x, const Tensor& y, const Scalar& rtol, const Scalar& atol, bool equal_nan);

PADDLE_API Tensor isfinite(const Tensor& x);

PADDLE_API Tensor isinf(const Tensor& x);

PADDLE_API Tensor isnan(const Tensor& x);

PADDLE_API Tensor kldiv_loss(const Tensor& x, const Tensor& label, const std::string& reduction);

PADDLE_API Tensor kron(const Tensor& x, const Tensor& y);

PADDLE_API std::tuple<Tensor,Tensor> kthvalue(const Tensor& x, int k, int axis, bool keepdim);

PADDLE_API Tensor label_smooth(const Tensor& label, paddle::optional<const Tensor&> prior_dist, float epsilon);

PADDLE_API Tensor leaky_relu(const Tensor& x, float alpha);

PADDLE_API Tensor lerp(const Tensor& x, const Tensor& y, const Tensor& weight);

PADDLE_API Tensor less_equal(const Tensor& x, const Tensor& y, int axis=-1);

PADDLE_API Tensor less_than(const Tensor& x, const Tensor& y, int axis=-1);

PADDLE_API Tensor lgamma(const Tensor& x);

PADDLE_API Tensor linspace(const Tensor& start, const Tensor& stop, const Tensor& number, DataType dtype);

PADDLE_API Tensor log(const Tensor& x);

PADDLE_API Tensor log10(const Tensor& x);

PADDLE_API Tensor log1p(const Tensor& x);

PADDLE_API Tensor log2(const Tensor& x);

PADDLE_API Tensor log_loss(const Tensor& input, const Tensor& label, float epsilon);

PADDLE_API Tensor log_softmax(const Tensor& x, int axis);

PADDLE_API Tensor logical_and(const Tensor& x, const Tensor& y);

PADDLE_API Tensor logical_not(const Tensor& x);

PADDLE_API Tensor logical_or(const Tensor& x, const Tensor& y);

PADDLE_API Tensor logical_xor(const Tensor& x, const Tensor& y);

PADDLE_API Tensor logit(const Tensor& x, float eps=1e-6f);

PADDLE_API Tensor logsigmoid(const Tensor& x);

PADDLE_API Tensor logsumexp(const Tensor& x, const std::vector<int64_t>& axis, bool keepdim, bool reduce_all);

PADDLE_API Tensor masked_select(const Tensor& x, const Tensor& mask);

PADDLE_API Tensor matmul(const Tensor& x, const Tensor& y, bool transpose_x=false, bool transpose_y=false);

PADDLE_API Tensor matrix_power(const Tensor& x, int n);

PADDLE_API Tensor matrix_rank(const Tensor& x, float tol, bool use_default_tol=true, bool hermitian=false);

PADDLE_API Tensor matrix_rank_tol(const Tensor& x, const Tensor& atol_tensor, bool use_default_tol=true, bool hermitian=false);

PADDLE_API Tensor max(const Tensor& x, const std::vector<int64_t>& dims={}, bool keep_dim=false);

PADDLE_API std::tuple<Tensor,Tensor> max_pool2d_with_index(const Tensor& x, const std::vector<int>& kernel_size, const std::vector<int>& strides, const std::vector<int>& paddings, bool global_pooling, bool adaptive);

PADDLE_API std::tuple<Tensor,Tensor> max_pool3d_with_index(const Tensor& x, const std::vector<int>& kernel_size, const std::vector<int>& strides, const std::vector<int>& paddings, bool global_pooling, bool adaptive);

PADDLE_API Tensor maximum(const Tensor& x, const Tensor& y);

PADDLE_API Tensor maxout(const Tensor& x, int groups, int axis);

PADDLE_API Tensor mean(const Tensor& x, const std::vector<int64_t>& dims={}, bool keep_dim=false);

PADDLE_API Tensor mean_all(const Tensor& x);

PADDLE_API std::vector<Tensor> meshgrid(const std::vector<Tensor>& inputs);

PADDLE_API Tensor min(const Tensor& x, const std::vector<int64_t>& dims={}, bool keep_dim=false);

PADDLE_API Tensor minimum(const Tensor& x, const Tensor& y);

PADDLE_API Tensor mish(const Tensor& x, float lambda);

PADDLE_API std::tuple<Tensor,Tensor> mode(const Tensor& x, int axis, bool keepdim);

PADDLE_API Tensor modulo(const Tensor& x, const Tensor& y);

PADDLE_API std::tuple<Tensor,Tensor,Tensor> momentum(const Tensor& param, const Tensor& grad, const Tensor& velocity, const Tensor& learning_rate, paddle::optional<const Tensor&> master_param, float mu, bool use_nesterov=false, const std::string& regularization_method="", float regularization_coeff=0.0, bool multi_precision=false, float rescale_grad=1.0f);

PADDLE_API Tensor multi_dot(const std::vector<Tensor>& x);

PADDLE_API Tensor multinomial(const Tensor& x, int num_samples, bool replacement);

PADDLE_API Tensor multiplex(const std::vector<Tensor>& ins, const Tensor& ids);

PADDLE_API Tensor multiply(const Tensor& x, const Tensor& y);

PADDLE_API Tensor mv(const Tensor& x, const Tensor& vec);

PADDLE_API std::tuple<Tensor,Tensor> nll_loss(const Tensor& input, const Tensor& label, paddle::optional<const Tensor&> weight, int64_t ignore_index, const std::string& reduction);

PADDLE_API Tensor norm(const Tensor& x, int axis, float epsilon, bool is_test);

PADDLE_API Tensor not_equal(const Tensor& x, const Tensor& y, int axis=-1);

PADDLE_API Tensor one_hot(const Tensor& x, const Scalar& num_classes);

PADDLE_API Tensor ones_like(const Tensor& x, DataType dtype=DataType::UNDEFINED, const Place& place={});

PADDLE_API Tensor p_norm(const Tensor& x, float porder, int axis, float epsilon, bool keepdim, bool asvector=false);

PADDLE_API Tensor pad(const Tensor& x, const std::vector<int>& paddings, float pad_value);

PADDLE_API Tensor pad3d(const Tensor& x, const IntArray& paddings, const std::string& mode, float pad_value, const std::string& data_format);

PADDLE_API Tensor pixel_shuffle(const Tensor& x, int upscale_factor, const std::string& data_format);

PADDLE_API Tensor poisson(const Tensor& x);

PADDLE_API Tensor pool2d(const Tensor& x, const std::vector<int>& kernel_size, const std::vector<int>& strides, const std::vector<int>& paddings, bool ceil_mode, bool exclusive, const std::string& data_format, const std::string& pooling_type, bool global_pooling, bool adaptive, const std::string& padding_algorithm);

PADDLE_API Tensor pool3d(const Tensor& x, const std::vector<int>& kernel_size, const std::vector<int>& strides, const std::vector<int>& paddings, bool ceil_mode, bool exclusive, const std::string& data_format, const std::string& pooling_type, bool global_pooling, bool adaptive, const std::string& padding_algorithm);

PADDLE_API Tensor pow(const Tensor& x, const Scalar& s);

PADDLE_API Tensor prelu(const Tensor& x, const Tensor& alpha, const std::string& data_format, const std::string& mode);

PADDLE_API Tensor psroi_pool(const Tensor& x, const Tensor& boxes, paddle::optional<const Tensor&> boxes_num, int pooled_height, int pooled_width, int output_channels, float spatial_scale);

PADDLE_API Tensor put_along_axis(const Tensor& x, const Tensor& index, const Tensor& value, int axis, const std::string& reduce);

PADDLE_API std::tuple<Tensor,Tensor> qr(const Tensor& x, const std::string& mode);

PADDLE_API Tensor randint(int low, int high, const IntArray& shape, DataType dtype=DataType::INT64, const Place& place={});

PADDLE_API Tensor randperm(int n, DataType dtype, const Place& place={});

PADDLE_API Tensor real(const Tensor& x);

PADDLE_API Tensor reciprocal(const Tensor& x);

PADDLE_API Tensor reduce_prod(const Tensor& x, const std::vector<int64_t>& dims, bool keep_dim, bool reduce_all);

PADDLE_API Tensor relu(const Tensor& x);

PADDLE_API Tensor relu_(const Tensor& x);

PADDLE_API Tensor reshape(const Tensor& x, const IntArray& shape);

PADDLE_API Tensor reshape_(const Tensor& x, const IntArray& shape);

PADDLE_API Tensor roi_align(const Tensor& x, const Tensor& boxes, paddle::optional<const Tensor&> boxes_num, int pooled_height, int pooled_width, float spatial_scale, int sampling_ratio, bool aligned);

PADDLE_API Tensor roi_pool(const Tensor& x, const Tensor& boxes, paddle::optional<const Tensor&> boxes_num, int pooled_height, int pooled_width, float spatial_scale);

PADDLE_API Tensor roll(const Tensor& x, const IntArray& shifts, const std::vector<int64_t>& axis);

PADDLE_API Tensor round(const Tensor& x);

PADDLE_API Tensor rsqrt(const Tensor& x);

PADDLE_API Tensor rsqrt_(const Tensor& x);

PADDLE_API Tensor scale(const Tensor& x, const Scalar& scale, float bias, bool bias_after_scale);

PADDLE_API Tensor scale_(const Tensor& x, const Scalar& scale, float bias, bool bias_after_scale);

PADDLE_API Tensor scatter(const Tensor& x, const Tensor& index, const Tensor& updates, bool overwrite);

PADDLE_API Tensor scatter_nd_add(const Tensor& x, const Tensor& index, const Tensor& updates);

PADDLE_API Tensor searchsorted(const Tensor& sorted_sequence, const Tensor& value, bool out_int32, bool right);

PADDLE_API std::tuple<Tensor,Tensor> segment_pool(const Tensor& x, const Tensor& segment_ids, const std::string& pooltype);

PADDLE_API Tensor selu(const Tensor& x, float scale, float alpha);

PADDLE_API Tensor shape(const Tensor& input);

PADDLE_API Tensor shard_index(const Tensor& in, int index_num, int nshards, int shard_id, int ignore_value);

PADDLE_API Tensor sigmoid(const Tensor& x);

PADDLE_API Tensor sigmoid_cross_entropy_with_logits(const Tensor& x, const Tensor& label, bool normalize, int ignore_index);

PADDLE_API Tensor sign(const Tensor& x);

PADDLE_API Tensor silu(const Tensor& x);

PADDLE_API Tensor sin(const Tensor& x);

PADDLE_API Tensor sinh(const Tensor& x);

PADDLE_API Tensor size(const Tensor& x);

PADDLE_API Tensor slice(const Tensor& input, const std::vector<int64_t>& axes, const IntArray& starts, const IntArray& ends, const std::vector<int64_t>& infer_flags, const std::vector<int64_t>& decrease_axis);

PADDLE_API Tensor soft_shrink(const Tensor& x, float lambda);

PADDLE_API Tensor softmax(const Tensor& x, int axis);

PADDLE_API std::vector<Tensor> split(const Tensor& x, const IntArray& num_or_sections, const Scalar& axis);

PADDLE_API Tensor sqrt(const Tensor& x);

PADDLE_API Tensor square(const Tensor& x);

PADDLE_API std::tuple<Tensor,Tensor> squeeze(const Tensor& x, const std::vector<int>& axes);

PADDLE_API Tensor stack(const std::vector<Tensor>& x, int axis);

PADDLE_API Tensor strided_slice(const Tensor& x, const std::vector<int>& axes, const IntArray& starts, const IntArray& ends, const IntArray& strides);

PADDLE_API Tensor subtract(const Tensor& x, const Tensor& y);

PADDLE_API Tensor sum(const Tensor& x, const std::vector<int64_t>& dims={}, DataType out_dtype=paddle::experimental::DataType::UNDEFINED, bool keep_dim=false);

PADDLE_API Tensor swish(const Tensor& x, float beta=1.0);

PADDLE_API Tensor take_along_axis(const Tensor& x, const Tensor& index, int axis);

PADDLE_API Tensor tan(const Tensor& x);

PADDLE_API Tensor tanh(const Tensor& x);

PADDLE_API Tensor tanh_shrink(const Tensor& x);

PADDLE_API Tensor thresholded_relu(const Tensor& x, float threshold);

PADDLE_API Tensor tile(const Tensor& x, const IntArray& repeat_times);

PADDLE_API std::tuple<Tensor,Tensor> top_k(const Tensor& x, const Scalar& k, int axis=-1, bool largest=true, bool sorted=true);

PADDLE_API Tensor trace(const Tensor& x, int offset, int axis1, int axis2);

PADDLE_API Tensor transpose(const Tensor& x, const std::vector<int>& axis);

PADDLE_API Tensor triangular_solve(const Tensor& x, const Tensor& y, bool upper, bool transpose, bool unitriangular);

PADDLE_API Tensor tril_triu(const Tensor& x, int diagonal, bool lower);

PADDLE_API Tensor trunc(const Tensor& x);

PADDLE_API Tensor truncated_gaussian_random(const std::vector<int>& shape, float mean, float std, int seed, DataType dtype=DataType::FLOAT32, const Place& place={});

PADDLE_API std::vector<Tensor> unbind(const Tensor& input, int axis);

PADDLE_API Tensor unfold(const Tensor& x, const std::vector<int>& kernel_sizes, const std::vector<int>& strides, const std::vector<int>& paddings, const std::vector<int>& dilations);

PADDLE_API Tensor uniform_random(const IntArray& shape, DataType dtype, float min, float max, int seed, const Place& place={});

PADDLE_API std::tuple<Tensor,Tensor,Tensor,Tensor> unique(const Tensor& x, bool return_index, bool return_inverse, bool return_counts, const std::vector<int>& axis, DataType dtype=DataType::INT64);

PADDLE_API std::tuple<Tensor,Tensor> unsqueeze(const Tensor& x, const IntArray& axis);

PADDLE_API std::tuple<Tensor,Tensor> viterbi_decode(const Tensor& input, const Tensor& transition, const Tensor& length, bool include_bos_eos_tag);

PADDLE_API Tensor where(const Tensor& condition, const Tensor& x, const Tensor& y);

PADDLE_API Tensor where_index(const Tensor& condition);

PADDLE_API std::tuple<Tensor,Tensor> yolo_box(const Tensor& x, const Tensor& img_size, const std::vector<int>& anchors, int class_num, float conf_thresh, int downsample_ratio, bool clip_bbox, float scale_x_y=1.0, bool iou_aware=false, float iou_aware_factor=0.5);

PADDLE_API Tensor zeros_like(const Tensor& x, DataType dtype=DataType::UNDEFINED, const Place& place={});


}  // namespace experimental
}  // namespace paddle
