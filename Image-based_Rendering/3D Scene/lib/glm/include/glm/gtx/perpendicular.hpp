#pragma once

// Dependency:
#include "../glm.hpp"
#include "../gtx/projection.hpp"

#ifndef GLM_ENABLE_EXPERIMENTAL
#error "GLM: GLM_GTX_perpendicular is an experimental extension and may change in the future. Use #define GLM_ENABLE_EXPERIMENTAL before including it, if you really want to use it."
#endif

#if GLM_MESSAGES == GLM_MESSAGES_ENABLED && !defined(GLM_EXT_INCLUDED)
#pragma message("GLM: GLM_GTX_perpendicular extension included")
#endif

namespace glm
{
/// @addtogroup gtx_perpendicular
/// @{

//! Projects x a perpendicular axis of Normal.
//! From GLM_GTX_perpendicular extension.
template <typename genType>
GLM_FUNC_DECL genType perp(genType const &x, genType const &Normal);

/// @}
} //namespace glm

#include "perpendicular.inl"