#pragma once

// Dependency:
#include "../common.hpp"
#include "../exponential.hpp"
#include "../geometric.hpp"

#ifndef GLM_ENABLE_EXPERIMENTAL
#error "GLM: GLM_GTX_fast_square_root is an experimental extension and may change in the future. Use #define GLM_ENABLE_EXPERIMENTAL before including it, if you really want to use it."
#endif

#if GLM_MESSAGES == GLM_MESSAGES_ENABLED && !defined(GLM_EXT_INCLUDED)
#pragma message("GLM: GLM_GTX_fast_square_root extension included")
#endif

namespace glm
{
/// @addtogroup gtx_fast_square_root
/// @{

/// Faster than the common sqrt function but less accurate.
///
/// @see gtx_fast_square_root extension.
template <typename genType>
GLM_FUNC_DECL genType fastSqrt(genType x);

/// Faster than the common sqrt function but less accurate.
///
/// @see gtx_fast_square_root extension.
template <length_t L, typename T, qualifier Q>
GLM_FUNC_DECL vec<L, T, Q> fastSqrt(vec<L, T, Q> const &x);

/// Faster than the common inversesqrt function but less accurate.
///
/// @see gtx_fast_square_root extension.
template <typename genType>
GLM_FUNC_DECL genType fastInverseSqrt(genType x);

/// Faster than the common inversesqrt function but less accurate.
///
/// @see gtx_fast_square_root extension.
template <length_t L, typename T, qualifier Q>
GLM_FUNC_DECL vec<L, T, Q> fastInverseSqrt(vec<L, T, Q> const &x);

/// Faster than the common length function but less accurate.
///
/// @see gtx_fast_square_root extension.
template <typename genType>
GLM_FUNC_DECL genType fastLength(genType x);

/// Faster than the common length function but less accurate.
///
/// @see gtx_fast_square_root extension.
template <length_t L, typename T, qualifier Q>
GLM_FUNC_DECL T fastLength(vec<L, T, Q> const &x);

/// Faster than the common distance function but less accurate.
///
/// @see gtx_fast_square_root extension.
template <typename genType>
GLM_FUNC_DECL genType fastDistance(genType x, genType y);

/// Faster than the common distance function but less accurate.
///
/// @see gtx_fast_square_root extension.
template <length_t L, typename T, qualifier Q>
GLM_FUNC_DECL T fastDistance(vec<L, T, Q> const &x, vec<L, T, Q> const &y);

/// Faster than the common normalize function but less accurate.
///
/// @see gtx_fast_square_root extension.
template <typename genType>
GLM_FUNC_DECL genType fastNormalize(genType const &x);

/// @}
} // namespace glm

#include "fast_square_root.inl"