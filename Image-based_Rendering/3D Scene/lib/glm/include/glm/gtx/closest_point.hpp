#pragma once

// Dependency:
#include "../glm.hpp"

#ifndef GLM_ENABLE_EXPERIMENTAL
#error "GLM: GLM_GTX_closest_point is an experimental extension and may change in the future. Use #define GLM_ENABLE_EXPERIMENTAL before including it, if you really want to use it."
#endif

#if GLM_MESSAGES == GLM_MESSAGES_ENABLED && !defined(GLM_EXT_INCLUDED)
#pragma message("GLM: GLM_GTX_closest_point extension included")
#endif

namespace glm
{
/// @addtogroup gtx_closest_point
/// @{

/// Find the point on a straight line which is the closet of a point.
/// @see gtx_closest_point
template <typename T, qualifier Q>
GLM_FUNC_DECL vec<3, T, Q> closestPointOnLine(
    vec<3, T, Q> const &point,
    vec<3, T, Q> const &a,
    vec<3, T, Q> const &b);

/// 2d lines work as well
template <typename T, qualifier Q>
GLM_FUNC_DECL vec<2, T, Q> closestPointOnLine(
    vec<2, T, Q> const &point,
    vec<2, T, Q> const &a,
    vec<2, T, Q> const &b);

/// @}
} // namespace glm

#include "closest_point.inl"