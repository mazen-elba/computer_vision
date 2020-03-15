#pragma once

// Dependencies
#include "../detail/setup.hpp"
#include "../detail/qualifier.hpp"
#include "../common.hpp"
#include "../integer.hpp"
#include "../exponential.hpp"
#include <limits>

#if GLM_MESSAGES == GLM_MESSAGES_ENABLED && !defined(GLM_EXT_INCLUDED)
#pragma message("GLM: GLM_GTC_integer extension included")
#endif

namespace glm
{
/// @addtogroup gtc_integer
/// @{

/// Returns the log2 of x for integer values. Can be reliably using to compute mipmap count from the texture size.
/// @see gtc_integer
template <typename genIUType>
GLM_FUNC_DECL genIUType log2(genIUType x);

/// Returns a value equal to the nearest integer to x.
/// The fraction 0.5 will round in a direction chosen by the
/// implementation, presumably the direction that is fastest.
///
/// @param x The values of the argument must be greater or equal to zero.
/// @tparam T floating point scalar types.
///
/// @see <a href="http://www.opengl.org/sdk/docs/manglsl/xhtml/round.xml">GLSL round man page</a>
/// @see gtc_integer
template <length_t L, typename T, qualifier Q>
GLM_FUNC_DECL vec<L, int, Q> iround(vec<L, T, Q> const &x);

/// Returns a value equal to the nearest integer to x.
/// The fraction 0.5 will round in a direction chosen by the
/// implementation, presumably the direction that is fastest.
///
/// @param x The values of the argument must be greater or equal to zero.
/// @tparam T floating point scalar types.
///
/// @see <a href="http://www.opengl.org/sdk/docs/manglsl/xhtml/round.xml">GLSL round man page</a>
/// @see gtc_integer
template <length_t L, typename T, qualifier Q>
GLM_FUNC_DECL vec<L, uint, Q> uround(vec<L, T, Q> const &x);

/// @}
} //namespace glm

#include "integer.inl"