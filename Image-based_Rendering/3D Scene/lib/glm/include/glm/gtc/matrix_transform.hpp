#pragma once

// Dependencies
#include "../mat4x4.hpp"
#include "../vec2.hpp"
#include "../vec3.hpp"
#include "../vec4.hpp"
#include "../gtc/constants.hpp"

#if GLM_MESSAGES == GLM_MESSAGES_ENABLED && !defined(GLM_EXT_INCLUDED)
#pragma message("GLM: GLM_GTC_matrix_transform extension included")
#endif

namespace glm
{
/// @addtogroup gtc_matrix_transform
/// @{

/// Builds a translation 4 * 4 matrix created from a vector of 3 components.
///
/// @param m Input matrix multiplied by this translation matrix.
/// @param v Coordinates of a translation vector.
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @code
/// #include <glm/glm.hpp>
/// #include <glm/gtc/matrix_transform.hpp>
/// ...
/// glm::mat4 m = glm::translate(glm::mat4(1.0f), glm::vec3(1.0f));
/// // m[0][0] == 1.0f, m[0][1] == 0.0f, m[0][2] == 0.0f, m[0][3] == 0.0f
/// // m[1][0] == 0.0f, m[1][1] == 1.0f, m[1][2] == 0.0f, m[1][3] == 0.0f
/// // m[2][0] == 0.0f, m[2][1] == 0.0f, m[2][2] == 1.0f, m[2][3] == 0.0f
/// // m[3][0] == 1.0f, m[3][1] == 1.0f, m[3][2] == 1.0f, m[3][3] == 1.0f
/// @endcode
/// @see gtc_matrix_transform
/// @see - translate(mat<4, 4, T, Q> const& m, T x, T y, T z)
/// @see - translate(vec<3, T, Q> const& v)
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glTranslate.xml">glTranslate man page</a>
template <typename T, qualifier Q>
GLM_FUNC_DECL mat<4, 4, T, Q> translate(
    mat<4, 4, T, Q> const &m, vec<3, T, Q> const &v);

/// Builds a rotation 4 * 4 matrix created from an axis vector and an angle.
///
/// @param m Input matrix multiplied by this rotation matrix.
/// @param angle Rotation angle expressed in radians.
/// @param axis Rotation axis, recommended to be normalized.
/// @tparam T Value type used to build the matrix. Supported: half, float or double.
/// @see gtc_matrix_transform
/// @see - rotate(mat<4, 4, T, Q> const& m, T angle, T x, T y, T z)
/// @see - rotate(T angle, vec<3, T, Q> const& v)
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glRotate.xml">glRotate man page</a>
template <typename T, qualifier Q>
GLM_FUNC_DECL mat<4, 4, T, Q> rotate(
    mat<4, 4, T, Q> const &m, T angle, vec<3, T, Q> const &axis);

/// Builds a scale 4 * 4 matrix created from 3 scalars.
///
/// @param m Input matrix multiplied by this scale matrix.
/// @param v Ratio of scaling for each axis.
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see - scale(mat<4, 4, T, Q> const& m, T x, T y, T z)
/// @see - scale(vec<3, T, Q> const& v)
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glScale.xml">glScale man page</a>
template <typename T, qualifier Q>
GLM_FUNC_DECL mat<4, 4, T, Q> scale(
    mat<4, 4, T, Q> const &m, vec<3, T, Q> const &v);

/// Creates a matrix for projecting two-dimensional coordinates onto the screen.
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see - glm::ortho(T const& left, T const& right, T const& bottom, T const& top, T const& zNear, T const& zFar)
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluOrtho2D.xml">gluOrtho2D man page</a>
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> ortho(
    T left, T right, T bottom, T top);

/// Creates a matrix for an orthographic parallel viewing volume, using left-handed coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see - glm::ortho(T const& left, T const& right, T const& bottom, T const& top)
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> orthoLH_ZO(
    T left, T right, T bottom, T top, T zNear, T zFar);

/// Creates a matrix for an orthographic parallel viewing volume using right-handed coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see - glm::ortho(T const& left, T const& right, T const& bottom, T const& top)
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> orthoLH_NO(
    T left, T right, T bottom, T top, T zNear, T zFar);

/// Creates a matrix for an orthographic parallel viewing volume, using left-handed coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see - glm::ortho(T const& left, T const& right, T const& bottom, T const& top)
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> orthoRH_ZO(
    T left, T right, T bottom, T top, T zNear, T zFar);

/// Creates a matrix for an orthographic parallel viewing volume, using right-handed coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see - glm::ortho(T const& left, T const& right, T const& bottom, T const& top)
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> orthoRH_NO(
    T left, T right, T bottom, T top, T zNear, T zFar);

/// Creates a matrix for an orthographic parallel viewing volume, using left-handed coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see - glm::ortho(T const& left, T const& right, T const& bottom, T const& top)
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> orthoZO(
    T left, T right, T bottom, T top, T zNear, T zFar);

/// Creates a matrix for an orthographic parallel viewing volume, using left-handed coordinates if GLM_FORCE_LEFT_HANDED if defined or right-handed coordinates otherwise.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see - glm::ortho(T const& left, T const& right, T const& bottom, T const& top)
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> orthoNO(
    T left, T right, T bottom, T top, T zNear, T zFar);

/// Creates a matrix for an orthographic parallel viewing volume, using left-handed coordinates.
/// If GLM_FORCE_DEPTH_ZERO_TO_ONE is defined, the near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
/// Otherwise, the near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see - glm::ortho(T const& left, T const& right, T const& bottom, T const& top)
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> orthoLH(
    T left, T right, T bottom, T top, T zNear, T zFar);

/// Creates a matrix for an orthographic parallel viewing volume, using right-handed coordinates.
/// If GLM_FORCE_DEPTH_ZERO_TO_ONE is defined, the near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
/// Otherwise, the near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see - glm::ortho(T const& left, T const& right, T const& bottom, T const& top)
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> orthoRH(
    T left, T right, T bottom, T top, T zNear, T zFar);

/// Creates a matrix for an orthographic parallel viewing volume, using the default handedness and default near and far clip planes definition.
/// To change default handedness use GLM_FORCE_LEFT_HANDED. To change default near and far clip planes definition use GLM_FORCE_DEPTH_ZERO_TO_ONE.
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see - glm::ortho(T const& left, T const& right, T const& bottom, T const& top)
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glOrtho.xml">glOrtho man page</a>
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> ortho(
    T left, T right, T bottom, T top, T zNear, T zFar);

/// Creates a left handed frustum matrix.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> frustumLH_ZO(
    T left, T right, T bottom, T top, T near, T far);

/// Creates a left handed frustum matrix.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> frustumLH_NO(
    T left, T right, T bottom, T top, T near, T far);

/// Creates a right handed frustum matrix.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> frustumRH_ZO(
    T left, T right, T bottom, T top, T near, T far);

/// Creates a right handed frustum matrix.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> frustumRH_NO(
    T left, T right, T bottom, T top, T near, T far);

/// Creates a frustum matrix using left-handed coordinates if GLM_FORCE_LEFT_HANDED if defined or right-handed coordinates otherwise.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> frustumZO(
    T left, T right, T bottom, T top, T near, T far);

/// Creates a frustum matrix using left-handed coordinates if GLM_FORCE_LEFT_HANDED if defined or right-handed coordinates otherwise.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> frustumNO(
    T left, T right, T bottom, T top, T near, T far);

/// Creates a left handed frustum matrix.
/// If GLM_FORCE_DEPTH_ZERO_TO_ONE is defined, the near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
/// Otherwise, the near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> frustumLH(
    T left, T right, T bottom, T top, T near, T far);

/// Creates a right handed frustum matrix.
/// If GLM_FORCE_DEPTH_ZERO_TO_ONE is defined, the near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
/// Otherwise, the near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> frustumRH(
    T left, T right, T bottom, T top, T near, T far);

/// Creates a frustum matrix with default handedness, using the default handedness and default near and far clip planes definition.
/// To change default handedness use GLM_FORCE_LEFT_HANDED. To change default near and far clip planes definition use GLM_FORCE_DEPTH_ZERO_TO_ONE.
///
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glFrustum.xml">glFrustum man page</a>
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> frustum(
    T left, T right, T bottom, T top, T near, T far);

/// Creates a matrix for a right handed, symetric perspective-view frustum.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveRH_ZO(
    T fovy, T aspect, T near, T far);

/// Creates a matrix for a right handed, symetric perspective-view frustum.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveRH_NO(
    T fovy, T aspect, T near, T far);

/// Creates a matrix for a left handed, symetric perspective-view frustum.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveLH_ZO(
    T fovy, T aspect, T near, T far);

/// Creates a matrix for a left handed, symetric perspective-view frustum.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveLH_NO(
    T fovy, T aspect, T near, T far);

/// Creates a matrix for a symetric perspective-view frustum using left-handed coordinates if GLM_FORCE_LEFT_HANDED if defined or right-handed coordinates otherwise.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveZO(
    T fovy, T aspect, T near, T far);

/// Creates a matrix for a symetric perspective-view frustum using left-handed coordinates if GLM_FORCE_LEFT_HANDED if defined or right-handed coordinates otherwise.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveNO(
    T fovy, T aspect, T near, T far);

/// Creates a matrix for a right handed, symetric perspective-view frustum.
/// If GLM_FORCE_DEPTH_ZERO_TO_ONE is defined, the near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
/// Otherwise, the near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveRH(
    T fovy, T aspect, T near, T far);

/// Creates a matrix for a left handed, symetric perspective-view frustum.
/// If GLM_FORCE_DEPTH_ZERO_TO_ONE is defined, the near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
/// Otherwise, the near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveLH(
    T fovy, T aspect, T near, T far);

/// Creates a matrix for a symetric perspective-view frustum based on the default handedness and default near and far clip planes definition.
/// To change default handedness use GLM_FORCE_LEFT_HANDED. To change default near and far clip planes definition use GLM_FORCE_DEPTH_ZERO_TO_ONE.
///
/// @param fovy Specifies the field of view angle in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluPerspective.xml">gluPerspective man page</a>
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspective(
    T fovy, T aspect, T near, T far);

/// Builds a perspective projection matrix based on a field of view using right-handed coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @param fov Expressed in radians.
/// @param width Width of the viewport
/// @param height Height of the viewport
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveFovRH_ZO(
    T fov, T width, T height, T near, T far);

/// Builds a perspective projection matrix based on a field of view using right-handed coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @param fov Expressed in radians.
/// @param width Width of the viewport
/// @param height Height of the viewport
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveFovRH_NO(
    T fov, T width, T height, T near, T far);

/// Builds a perspective projection matrix based on a field of view using left-handed coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @param fov Expressed in radians.
/// @param width Width of the viewport
/// @param height Height of the viewport
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveFovLH_ZO(
    T fov, T width, T height, T near, T far);

/// Builds a perspective projection matrix based on a field of view using left-handed coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @param fov Expressed in radians.
/// @param width Width of the viewport
/// @param height Height of the viewport
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveFovLH_NO(
    T fov, T width, T height, T near, T far);

/// Builds a perspective projection matrix based on a field of view using left-handed coordinates if GLM_FORCE_LEFT_HANDED if defined or right-handed coordinates otherwise.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @param fov Expressed in radians.
/// @param width Width of the viewport
/// @param height Height of the viewport
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveFovZO(
    T fov, T width, T height, T near, T far);

/// Builds a perspective projection matrix based on a field of view using left-handed coordinates if GLM_FORCE_LEFT_HANDED if defined or right-handed coordinates otherwise.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @param fov Expressed in radians.
/// @param width Width of the viewport
/// @param height Height of the viewport
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveFovNO(
    T fov, T width, T height, T near, T far);

/// Builds a right handed perspective projection matrix based on a field of view.
/// If GLM_FORCE_DEPTH_ZERO_TO_ONE is defined, the near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
/// Otherwise, the near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @param fov Expressed in radians.
/// @param width Width of the viewport
/// @param height Height of the viewport
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveFovRH(
    T fov, T width, T height, T near, T far);

/// Builds a left handed perspective projection matrix based on a field of view.
/// If GLM_FORCE_DEPTH_ZERO_TO_ONE is defined, the near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
/// Otherwise, the near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @param fov Expressed in radians.
/// @param width Width of the viewport
/// @param height Height of the viewport
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveFovLH(
    T fov, T width, T height, T near, T far);

/// Builds a perspective projection matrix based on a field of view and the default handedness and default near and far clip planes definition.
/// To change default handedness use GLM_FORCE_LEFT_HANDED. To change default near and far clip planes definition use GLM_FORCE_DEPTH_ZERO_TO_ONE.
///
/// @param fov Expressed in radians.
/// @param width Width of the viewport
/// @param height Height of the viewport
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param far Specifies the distance from the viewer to the far clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> perspectiveFov(
    T fov, T width, T height, T near, T far);

/// Creates a matrix for a left handed, symmetric perspective-view frustum with far plane at infinite.
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> infinitePerspectiveLH(
    T fovy, T aspect, T near);

/// Creates a matrix for a right handed, symmetric perspective-view frustum with far plane at infinite.
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> infinitePerspectiveRH(
    T fovy, T aspect, T near);

/// Creates a matrix for a symmetric perspective-view frustum with far plane at infinite with default handedness.
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> infinitePerspective(
    T fovy, T aspect, T near);

/// Creates a matrix for a symmetric perspective-view frustum with far plane at infinite for graphics hardware that doesn't support depth clamping.
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> tweakedInfinitePerspective(
    T fovy, T aspect, T near);

/// Creates a matrix for a symmetric perspective-view frustum with far plane at infinite for graphics hardware that doesn't support depth clamping.
///
/// @param fovy Specifies the field of view angle, in degrees, in the y direction. Expressed in radians.
/// @param aspect Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
/// @param near Specifies the distance from the viewer to the near clipping plane (always positive).
/// @param ep Epsilon
/// @tparam T Value type used to build the matrix. Currently supported: half (not recommended), float or double.
/// @see gtc_matrix_transform
template <typename T>
GLM_FUNC_DECL mat<4, 4, T, defaultp> tweakedInfinitePerspective(
    T fovy, T aspect, T near, T ep);

/// Map the specified object coordinates (obj.x, obj.y, obj.z) into window coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @param obj Specify the object coordinates.
/// @param model Specifies the current modelview matrix
/// @param proj Specifies the current projection matrix
/// @param viewport Specifies the current viewport
/// @return Return the computed window coordinates.
/// @tparam T Native type used for the computation. Currently supported: half (not recommended), float or double.
/// @tparam U Currently supported: Floating-point types and integer types.
/// @see gtc_matrix_transform
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluProject.xml">gluProject man page</a>
template <typename T, typename U, qualifier Q>
GLM_FUNC_DECL vec<3, T, Q> projectZO(
    vec<3, T, Q> const &obj, mat<4, 4, T, Q> const &model, mat<4, 4, T, Q> const &proj, vec<4, U, Q> const &viewport);

/// Map the specified object coordinates (obj.x, obj.y, obj.z) into window coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @param obj Specify the object coordinates.
/// @param model Specifies the current modelview matrix
/// @param proj Specifies the current projection matrix
/// @param viewport Specifies the current viewport
/// @return Return the computed window coordinates.
/// @tparam T Native type used for the computation. Currently supported: half (not recommended), float or double.
/// @tparam U Currently supported: Floating-point types and integer types.
/// @see gtc_matrix_transform
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluProject.xml">gluProject man page</a>
template <typename T, typename U, qualifier Q>
GLM_FUNC_DECL vec<3, T, Q> projectNO(
    vec<3, T, Q> const &obj, mat<4, 4, T, Q> const &model, mat<4, 4, T, Q> const &proj, vec<4, U, Q> const &viewport);

/// Map the specified object coordinates (obj.x, obj.y, obj.z) into window coordinates using default near and far clip planes definition.
/// To change default near and far clip planes definition use GLM_FORCE_DEPTH_ZERO_TO_ONE.
///
/// @param obj Specify the object coordinates.
/// @param model Specifies the current modelview matrix
/// @param proj Specifies the current projection matrix
/// @param viewport Specifies the current viewport
/// @return Return the computed window coordinates.
/// @tparam T Native type used for the computation. Currently supported: half (not recommended), float or double.
/// @tparam U Currently supported: Floating-point types and integer types.
/// @see gtc_matrix_transform
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluProject.xml">gluProject man page</a>
template <typename T, typename U, qualifier Q>
GLM_FUNC_DECL vec<3, T, Q> project(
    vec<3, T, Q> const &obj, mat<4, 4, T, Q> const &model, mat<4, 4, T, Q> const &proj, vec<4, U, Q> const &viewport);

/// Map the specified window coordinates (win.x, win.y, win.z) into object coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of 0 and +1 respectively. (Direct3D clip volume definition)
///
/// @param win Specify the window coordinates to be mapped.
/// @param model Specifies the modelview matrix
/// @param proj Specifies the projection matrix
/// @param viewport Specifies the viewport
/// @return Returns the computed object coordinates.
/// @tparam T Native type used for the computation. Currently supported: half (not recommended), float or double.
/// @tparam U Currently supported: Floating-point types and integer types.
/// @see gtc_matrix_transform
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluUnProject.xml">gluUnProject man page</a>
template <typename T, typename U, qualifier Q>
GLM_FUNC_DECL vec<3, T, Q> unProjectZO(
    vec<3, T, Q> const &win, mat<4, 4, T, Q> const &model, mat<4, 4, T, Q> const &proj, vec<4, U, Q> const &viewport);

/// Map the specified window coordinates (win.x, win.y, win.z) into object coordinates.
/// The near and far clip planes correspond to z normalized device coordinates of -1 and +1 respectively. (OpenGL clip volume definition)
///
/// @param win Specify the window coordinates to be mapped.
/// @param model Specifies the modelview matrix
/// @param proj Specifies the projection matrix
/// @param viewport Specifies the viewport
/// @return Returns the computed object coordinates.
/// @tparam T Native type used for the computation. Currently supported: half (not recommended), float or double.
/// @tparam U Currently supported: Floating-point types and integer types.
/// @see gtc_matrix_transform
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluUnProject.xml">gluUnProject man page</a>
template <typename T, typename U, qualifier Q>
GLM_FUNC_DECL vec<3, T, Q> unProjectNO(
    vec<3, T, Q> const &win, mat<4, 4, T, Q> const &model, mat<4, 4, T, Q> const &proj, vec<4, U, Q> const &viewport);

/// Map the specified window coordinates (win.x, win.y, win.z) into object coordinates using default near and far clip planes definition.
/// To change default near and far clip planes definition use GLM_FORCE_DEPTH_ZERO_TO_ONE.
///
/// @param win Specify the window coordinates to be mapped.
/// @param model Specifies the modelview matrix
/// @param proj Specifies the projection matrix
/// @param viewport Specifies the viewport
/// @return Returns the computed object coordinates.
/// @tparam T Native type used for the computation. Currently supported: half (not recommended), float or double.
/// @tparam U Currently supported: Floating-point types and integer types.
/// @see gtc_matrix_transform
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluUnProject.xml">gluUnProject man page</a>
template <typename T, typename U, qualifier Q>
GLM_FUNC_DECL vec<3, T, Q> unProject(
    vec<3, T, Q> const &win, mat<4, 4, T, Q> const &model, mat<4, 4, T, Q> const &proj, vec<4, U, Q> const &viewport);

/// Define a picking region
///
/// @param center Specify the center of a picking region in window coordinates.
/// @param delta Specify the width and height, respectively, of the picking region in window coordinates.
/// @param viewport Rendering viewport
/// @tparam T Native type used for the computation. Currently supported: half (not recommended), float or double.
/// @tparam U Currently supported: Floating-point types and integer types.
/// @see gtc_matrix_transform
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluPickMatrix.xml">gluPickMatrix man page</a>
template <typename T, qualifier Q, typename U>
GLM_FUNC_DECL mat<4, 4, T, Q> pickMatrix(
    vec<2, T, Q> const &center, vec<2, T, Q> const &delta, vec<4, U, Q> const &viewport);

/// Build a right handed look at view matrix.
///
/// @param eye Position of the camera
/// @param center Position where the camera is looking at
/// @param up Normalized up vector, how the camera is oriented. Typically (0, 0, 1)
/// @see gtc_matrix_transform
/// @see - frustum(T const& left, T const& right, T const& bottom, T const& top, T const& nearVal, T const& farVal) frustum(T const& left, T const& right, T const& bottom, T const& top, T const& nearVal, T const& farVal)
template <typename T, qualifier Q>
GLM_FUNC_DECL mat<4, 4, T, Q> lookAtRH(
    vec<3, T, Q> const &eye, vec<3, T, Q> const &center, vec<3, T, Q> const &up);

/// Build a left handed look at view matrix.
///
/// @param eye Position of the camera
/// @param center Position where the camera is looking at
/// @param up Normalized up vector, how the camera is oriented. Typically (0, 0, 1)
/// @see gtc_matrix_transform
/// @see - frustum(T const& left, T const& right, T const& bottom, T const& top, T const& nearVal, T const& farVal) frustum(T const& left, T const& right, T const& bottom, T const& top, T const& nearVal, T const& farVal)
template <typename T, qualifier Q>
GLM_FUNC_DECL mat<4, 4, T, Q> lookAtLH(
    vec<3, T, Q> const &eye, vec<3, T, Q> const &center, vec<3, T, Q> const &up);

/// Build a look at view matrix based on the default handedness.
///
/// @param eye Position of the camera
/// @param center Position where the camera is looking at
/// @param up Normalized up vector, how the camera is oriented. Typically (0, 0, 1)
/// @see gtc_matrix_transform
/// @see - frustum(T const& left, T const& right, T const& bottom, T const& top, T const& nearVal, T const& farVal) frustum(T const& left, T const& right, T const& bottom, T const& top, T const& nearVal, T const& farVal)
/// @see <a href="https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml">gluLookAt man page</a>
template <typename T, qualifier Q>
GLM_FUNC_DECL mat<4, 4, T, Q> lookAt(
    vec<3, T, Q> const &eye, vec<3, T, Q> const &center, vec<3, T, Q> const &up);

/// @}
} //namespace glm

#include "matrix_transform.inl"