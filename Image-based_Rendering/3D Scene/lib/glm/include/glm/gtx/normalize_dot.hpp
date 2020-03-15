#pragma once

// Dependency:
#include "../gtx/fast_square_root.hpp"

#ifndef GLM_ENABLE_EXPERIMENTAL
#error "GLM: GLM_GTX_normalize_dot is an experimental extension and may change in the future. Use #define GLM_ENABLE_EXPERIMENTAL before including it, if you really want to use it."
#endif

#if GLM_MESSAGES == GLM_MESSAGES_ENABLED && !defined(GLM_EXT_INCLUDED)
#pragma message("GLM: GLM_GTX_normalize_dot extension included")
#endif

namespace glm
{
/// @addtogroup gtx_normalize_dot
/// @{

/// Normalize parameters and returns the dot product of x and y.
/// It's faster that dot(normalize(x), normalize(y)).
///
/// @see gtx_normalize_dot extension.
template <length_t L, typename T, qualifier Q>
GLM_FUNC_DECL T normalizeDot(vec<L, T, Q> const &x, vec<L, T, Q> const &y);

/// Normalize parameters and returns the dot product of x and y.
/// Faster that dot(fastNormalize(x), fastNormalize(y)).
///
/// @see gtx_normalize_dot extension.
template <length_t L, typename T, qualifier Q>
GLM_FUNC_DECL T fastNormalizeDot(vec<L, T, Q> const &x, vec<L, T, Q> const &y);

/// @}
} //namespace glm

#include "normalize_dot.inl"