#pragma once

// Dependency:
#include "../glm.hpp"

#ifndef GLM_ENABLE_EXPERIMENTAL
#error "GLM: GLM_GTX_normal is an experimental extension and may change in the future. Use #define GLM_ENABLE_EXPERIMENTAL before including it, if you really want to use it."
#endif

#if GLM_MESSAGES == GLM_MESSAGES_ENABLED && !defined(GLM_EXT_INCLUDED)
#pragma message("GLM: GLM_GTX_normal extension included")
#endif

namespace glm
{
/// @addtogroup gtx_normal
/// @{

/// Computes triangle normal from triangle points.
///
/// @see gtx_normal
template <typename T, qualifier Q>
GLM_FUNC_DECL vec<3, T, Q> triangleNormal(vec<3, T, Q> const &p1, vec<3, T, Q> const &p2, vec<3, T, Q> const &p3);

/// @}
} //namespace glm

#include "normal.inl"