#pragma once

// Dependencies
#include "../detail/setup.hpp"
#include "../detail/qualifier.hpp"
#include "../vec3.hpp"
#include <limits>

#if GLM_MESSAGES == GLM_MESSAGES_ENABLED && !defined(GLM_EXT_INCLUDED)
#pragma message("GLM: GLM_GTC_color_encoding extension included")
#endif

namespace glm
{
/// @addtogroup gtx_color_encoding
/// @{

/// Convert a linear sRGB color to D65 YUV.
template <typename T, qualifier Q>
GLM_FUNC_DECL vec<3, T, Q> convertLinearSRGBToD65XYZ(vec<3, T, Q> const &ColorLinearSRGB);

/// Convert a linear sRGB color to D50 YUV.
template <typename T, qualifier Q>
GLM_FUNC_DECL vec<3, T, Q> convertLinearSRGBToD50XYZ(vec<3, T, Q> const &ColorLinearSRGB);

/// Convert a D65 YUV color to linear sRGB.
template <typename T, qualifier Q>
GLM_FUNC_DECL vec<3, T, Q> convertD65XYZToLinearSRGB(vec<3, T, Q> const &ColorD65XYZ);

/// Convert a D65 YUV color to D50 YUV.
template <typename T, qualifier Q>
GLM_FUNC_DECL vec<3, T, Q> convertD65XYZToD50XYZ(vec<3, T, Q> const &ColorD65XYZ);

/// @}
} //namespace glm

#include "color_encoding.inl"