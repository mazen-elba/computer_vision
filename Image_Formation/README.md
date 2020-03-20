# Geometric Primitives & Transformatinos

## Geomtric Primitives

**2D Points (pixel coordinates)** \
Since ![img](http://latex.codecogs.com/svg.latex?%5Cmathbb%7BP%7D%5E2%20%3D%20%5Cmathbb%7BR%7D%5E3%20-%20%280%2C%200%2C%200%29) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bx%7D%20%3D%20%28x%2C%20y%29%20%5Cin%20%5Cmathbb%7BR%7D%5E2%20%3D%20%5Cbegin%7Bbmatrix%7D%20x%5C%5C%20y%5C%5C%20%5Cend%7Bbmatrix%7D) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Bx%7D%7D%20%3D%20%28%5Ctilde%7Bx%7D%2C%20%5Ctilde%7By%7D%2C%20%5Ctilde%7Bw%7D%29%20%5Cin%20%5Cmathbb%7BP%7D%5E2%20%3D%20%5Ctilde%7Bw%7D%28x%2Cy%2C1%29%20%3D%20%5Ctilde%7Bw%7D%20%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D) \
where ![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D%20%3D%20%28x%2C%20y%2C%201%29) is the augmented vector

**2D Lines** \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Bl%7D%7D%20%3D%20%28a%2C%20b%2C%20c%29) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D%5Ccdot%20%5Cboldsymbol%7B%5Ctilde%7Bl%7D%7D%20%3D%20ax%20+%20by%20+%20c%20%3D%200) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bl%7D%20%3D%20%28%5Ctilde%7Bn%7D_x%2C%20%5Ctilde%7Bn%7D_y%2C%20d%29%20%3D%20%28%5Cboldsymbol%7B%5Ctilde%7Bn%7D%7D%2C%20d%29) with ![img](http://latex.codecogs.com/svg.latex?%5Cleft%20%5C%7C%20%5Chat%7B%5Cmathbf%7Bn%7D%7D%5Cright%20%5C%7C%20%3D%201) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Bl%7D%7D%20%3D%20%280%2C%200%2C%201%29) \
![img](http://latex.codecogs.com/svg.latex?%5Ctheta%20%2C%20%5Cboldsymbol%7B%5Ctilde%7Bn%7D%7D%20%3D%20%28%5Ctilde%7Bn%7D_x%2C%20%5Ctilde%7Bn%7D_y%29%20%3D%20%28cos%5Ctheta%2C%20sin%5Ctheta%29) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Bx%7D%7D%20%3D%20%5Cboldsymbol%7B%5Ctilde%7Bl%7D_1%7D%20%5Ctimes%20%5Cboldsymbol%7B%5Ctilde%7Bl%7D_2%7D) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Bl%7D%7D%20%3D%20%5Cboldsymbol%7B%5Ctilde%7Bx%7D_1%7D%20%5Ctimes%20%5Cboldsymbol%7B%5Ctilde%7Bx%7D_2%7D)

**2D Conics** \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Bx%7D%7D%5ET%5Cboldsymbol%7B%5Cmathbb%7BQ%7D%7D%5Cboldsymbol%7B%5Ctilde%7Bx%7D%7D%20%3D%200)

**3D Points** \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bx%7D%20%3D%20%28x%2C%20y%2C%20z%29%20%5Cin%20%5Cmathbb%7BR%7D%5E3) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Bx%7D%7D%20%3D%20%28%5Ctilde%7Bx%7D%2C%20%5Ctilde%7By%7D%2C%20%5Ctilde%7Bz%7D%2C%20%5Ctilde%7Bw%7D%29%20%5Cin%20%5Cmathbb%7BP%7D%5E3) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D%20%3D%20%28x%2C%20y%2C%20z%2C%201%29) with ![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Bx%7D%7D%20%3D%20%5Ctilde%7Bw%7D%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D)

**3D Planes** \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Bm%7D%7D%20%3D%20%28a%2C%20b%2C%20c%2C%20d%29) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D%20%5Ccdot%20%5Cboldsymbol%7B%5Ctilde%7Bm%7D%7D%20%3D%20ax%20+%20by%20+%20cz%20+%20d%20%3D%200) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bm%7D%20%3D%20%28%5Ctilde%7Bn%7D_x%2C%20%5Ctilde%7Bn%7D_y%2C%20%5Ctilde%7Bn%7D_z%2C%20d%29%20%3D%20%28%5Cboldsymbol%7B%5Ctilde%7Bn%7D%7D%2C%20d%29) with ![img](http://latex.codecogs.com/svg.latex?%5Cleft%20%5C%7C%20%5Cboldsymbol%7B%5Ctilde%7Bn%7D%7D%20%5Cright%20%5C%7C%20%3D%201) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Bm%7D%7D%20%3D%20%280%2C%200%2C%200%2C%201%29) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Bn%7D%7D%20%3D%20%28cos%20%5Ctheta%20cos%20%5Cphi%2C%20sin%20%5Ctheta%20cos%20%5Cphi%2C%20sin%20%5Cphi%29)

**3D Lines** \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Br%7D%20%3D%20%281%20-%20%5Clambda%29%5Cboldsymbol%7Bp%7D%20+%20%5Clambda%20%5Cboldsymbol%7Bq%7D) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Br%7D%7D%20%3D%20%5Cmu%20%5Cboldsymbol%7B%5Ctilde%7Bp%7D%7D%20+%20%5Clambda%20%5Cboldsymbol%7B%5Ctilde%7Bq%7D%7D) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Ctilde%7Bq%7D%7D%20%3D%20%28%5Ctilde%7Bd%7D_x%2C%20%5Ctilde%7Bd%7D_y%2C%20%5Ctilde%7Bd%7D_z%2C%200%29%20%3D%20%28%5Cboldsymbol%7B%5Ctilde%7Bd%7D%7D%2C%200%29) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Br%7D%20%3D%20%5Cboldsymbol%7Bp%7D%20+%20%5Clambda%20%5Cboldsymbol%7B%5Ctilde%7Bd%7D%7D) \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7BL%7D%20%3D%20%5Cboldsymbol%7B%5Ctilde%7Bp%7D%7D%20%5Cboldsymbol%7B%5Ctilde%7Bq%7D%7D%5ET%20-%20%5Cboldsymbol%7B%5Ctilde%7Bq%7D%7D%20%5Cboldsymbol%7B%5Ctilde%7Bp%7D%7D%5ET) \
![img](http://latex.codecogs.com/svg.latex?det%28%5Cboldsymbol%7BL%7D%29%20%3D%200)

**3D Quadrics** \
![img](http://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D%5ET%20%5Cmathbb%7BQ%7D%20%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D%20%3D%200)

## 2D Transformations

**Translation** \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7B%7Bx%7D%27%7D%20%3D%20%5Cboldsymbol%7Bx%7D%20+%20%5Cboldsymbol%7Bt%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7BI%7D%20%26%20%5Cboldsymbol%7Bt%7D%20%5Cend%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D) \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7B%7B%5Cbar%7Bx%7D%7D%27%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7BI%7D%20%26%20%5Cboldsymbol%7Bt%7D%20%5C%5C%20%5Cboldsymbol%7B0%7D%5ET%20%26%201%20%5Cend%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D)

**Rotation & Translation** \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7B%7Bx%7D%27%7D%20%3D%20%5Cboldsymbol%7BRx%7D%20+%20%5Cboldsymbol%7Bt%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7BR%7D%20%26%20%5Cboldsymbol%7Bt%7D%20%5Cend%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D) \
where ![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7BR%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20cos%5Ctheta%20%26%20-sin%5Ctheta%5C%5C%20sin%5Ctheta%20%26%20cos%5Ctheta%20%5Cend%7Bbmatrix%7D) \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7BR%7D%20%5Cboldsymbol%7BR%7D%5ET%20%3D%20%5Cboldsymbol%7BI%7D) and ![img](http://latex.codecogs.com/gif.latex?%5Cleft%20%7C%20%5Cboldsymbol%7BR%7D%20%5Cright%20%7C%20%3D%201)

**Scaled Rotation** \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7Bx%7D%27%20%3D%20s%5Cboldsymbol%7BRx%7D%20+%20%5Cboldsymbol%7Bt%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20s%5Cboldsymbol%7BR%7D%20%26%20%5Cboldsymbol%7Bt%7D%20%5Cend%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20a%20%26%20-b%20%26%20t_x%5C%5C%20b%20%26%20a%20%26%20t_y%20%5Cend%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D)

**Affine** \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7Bx%7D%27%20%3D%20%5Cboldsymbol%7BA%5Cbar%7Bx%7D%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20a_%7B00%7D%20%26%20a_%7B01%7D%20%26%20a_%7B02%7D%5C%5C%20a_%7B10%7D%20%26%20a_%7B11%7D%20%26%20a_%7B12%7D%20%5Cend%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D)

**Projective** \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7B%5Ctilde%7Bx%7D%7D%27%20%3D%20%5Cboldsymbol%7B%5Ctilde%7BH%7D%5Ctilde%7Bx%7D%7D) \
![img](http://latex.codecogs.com/gif.latex?x%27%20%3D%20%5Cfrac%7Bh_%7B00%7Dx%20+%20h_%7B01%7Dy%20+%20h_%7B02%7D%7D%7Bh_%7B20%7Dx%20+%20h_%7B21%7Dy%20+%20h_%7B22%7D%7D) and ![img](http://latex.codecogs.com/gif.latex?y%27%20%3D%20%5Cfrac%7Bh_%7B10%7Dx%20+%20h_%7B11%7Dy%20+%20h_%7B12%7D%7D%7Bh_%7B20%7Dx%20+%20h_%7B21%7Dy%20+%20h_%7B22%7D%7D)

**Co-Vectors** \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7B%5Ctilde%7Bl%7D%7D%27%20%5Ccdot%20%5Cboldsymbol%7B%5Ctilde%7Bx%7D%7D%27%20%3D%20%5Cboldsymbol%7B%5Ctilde%7Bl%7D%7D%27%5ET%20%5Cboldsymbol%7B%5Ctilde%7BH%7D%7D%20%5Cboldsymbol%7B%5Ctilde%7Bx%7D%7D%20%3D%20%28%5Cboldsymbol%7B%5Ctilde%7BH%7D%7D%5ET%20%5Cboldsymbol%7B%5Ctilde%7Bl%7D%7D%27%29%5ET%20%5Cboldsymbol%7B%5Ctilde%7Bx%7D%7D%20%3D%20%5Cboldsymbol%7B%5Ctilde%7Bl%7D%7D%20%5Ccdot%20%5Cboldsymbol%7B%5Ctilde%7Bx%7D%7D%20%3D%200) \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7B%5Ctilde%7Bl%7D%7D%27%20%3D%20%5Cboldsymbol%7B%5Ctilde%7BH%7D%7D%5E%7B-T%7D%20%5Cboldsymbol%7B%5Ctilde%7Bl%7D%7D)

**Stretch/Squash** \
![img](http://latex.codecogs.com/gif.latex?x%27%20%3D%20s_xx%20+%20t_x) \
![img](http://latex.codecogs.com/gif.latex?y%27%20%3D%20s_yy%20+%20t_y)

**Planar Surface Flow** \
![img](http://latex.codecogs.com/gif.latex?x%27%20%3D%20a_0%20+%20a_1x%20+%20a_2y%20+%20a_6x%5E2%20+%20a_7xy) \
![img](http://latex.codecogs.com/gif.latex?y%27%20%3D%20a_3%20+%20a_4x%20+%20a_5y%20+%20a_7x%5E2%20+%20a_6xy)

**Bilinear Interpolant** \
![img](http://latex.codecogs.com/gif.latex?x%27%20%3D%20a_0%20+%20a_1x%20+%20a_2y%20+%20a_6xy) \
![img](http://latex.codecogs.com/gif.latex?y%27%20%3D%20a_3%20+%20a_4x%20+%20a_5y%20+%20a_7xy)

## 3D Transformations

**Translation** \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7Bx%7D%27%20%3D%20%5Cboldsymbol%7Bx%7D%20+%20%5Cboldsymbol%7Bt%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7BI%7D%20%26%20%5Cboldsymbol%7Bt%7D%20%5Cend%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D)

**Roation & Translation** \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7Bx%7D%27%20%3D%20%5Cboldsymbol%7BRx%7D%20+%20%5Cboldsymbol%7Bt%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7BR%7D%20%26%20%5Cboldsymbol%7Bt%7D%20%5Cend%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D) \
where ![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7BRR%7D%5ET%20%3D%20%5Cboldsymbol%7BI%7D) and ![img](http://latex.codecogs.com/gif.latex?%5Cleft%20%7C%5Cboldsymbol%7BR%7D%20%5Cright%20%7C%20%3D%201) \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7Bx%7D%27%20%3D%20%5Cboldsymbol%7BR%7D%20%28%5Cboldsymbol%7Bx%7D%20-%20%5Cboldsymbol%7Bc%7D%29%20%3D%20%5Cboldsymbol%7BRx%7D%20-%20%5Cboldsymbol%7BRc%7D)

**Scaled Rotation** \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7Bx%7D%27%20%3D%20s%5Cboldsymbol%7BRx%7D%20+%20%5Cboldsymbol%7Bt%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20s%5Cboldsymbol%7BR%7D%20%26%20%5Cboldsymbol%7Bt%7D%20%5Cend%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D)

**Affine** \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7Bx%7D%27%20%3D%20%5Cboldsymbol%7BA%5Cbar%7Bx%7D%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20a_%7B00%7D%20%26%20a_%7B01%7D%20%26%20a_%7B02%7D%20%26%20a_%7B03%7D%20%5C%5C%20a_%7B10%7D%20%26%20a_%7B11%7D%20%26%20a_%7B12%7D%20%26%20a_%7B13%7D%20%5C%5C%20a_%7B20%7D%20%26%20a_%7B21%7D%20%26%20a_%7B22%7D%20%26%20a_%7B23%7D%20%5Cend%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Cbar%7Bx%7D%7D)

**Projective** \
![img](http://latex.codecogs.com/gif.latex?%5Cboldsymbol%7B%5Ctilde%7Bx%7D%7D%27%20%3D%20%5Cboldsymbol%7B%5Ctilde%7BA%7D%5Ctilde%7Bx%7D%7D)

## 3D Rotations

**Axis/Angle (exponential twist)** \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Comega%7D%20%3D%20%5Ctheta%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bv_%7B%5Cparallel%20%7D%7D%20%3D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%28%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Ccdot%20%5Cboldsymbol%7Bv%7D%29%20%3D%20%28%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%5ET%29%20%5Cboldsymbol%7Bv%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bv_%7B%5Cperp%7D%7D%20%3D%20%5Cboldsymbol%7Bv%7D%20-%20%5Cboldsymbol%7Bv_%5Cparallel%7D%20%3D%20%28%5Cboldsymbol%7BI%7D%20-%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%5ET%29%20%5Cboldsymbol%7Bv%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bv_%7B%5Ctimes%7D%7D%20%3D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Ctimes%20%5Cboldsymbol%7Bv%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20%5Cboldsymbol%7Bv%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%3D%20%28%5Chat%7Bn%7D_x%2C%20%5Chat%7Bn%7D_y%2C%20%5Chat%7Bn%7D_z%29) \
![img](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%200%20%26%20-%5Chat%7Bn%7D_z%20%26%20%5Chat%7Bn%7D_y%20%5C%5C%20%5Chat%7Bn%7D_z%20%26%200%20%26%20-%5Chat%7Bn%7D_x%20%5C%5C%20-%5Chat%7Bn%7D_y%20%26%20%5Chat%7Bn%7D_x%20%26%200%20%5Cend%7Bbmatrix%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bv%7D_%7B%5Ctimes%5Ctimes%7D%20%3D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Ctimes%20%5Cboldsymbol%7Bv%7D_%7B%5Ctimes%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E2%20%5Cboldsymbol%7Bv%7D%20%3D%20-%5Cboldsymbol%7Bv%7D_%7B%5Cperp%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bv%7D_%7B%5Cparallel%7D%20%3D%20%5Cboldsymbol%7Bv%7D%20-%20%5Cboldsymbol%7Bv%7D_%7B%5Cperp%7D%20%3D%20%5Cboldsymbol%7Bv%7D%20+%20%5Cboldsymbol%7Bv%7D_%7B%5Ctimes%5Ctimes%7D%20%3D%20%28%20%5Cboldsymbol%7BI%7D%20+%20%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E2%29%20%5Cboldsymbol%7Bv%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bu%7D_%7B%5Cperp%7D%20%3D%20cos%5Ctheta%5Cboldsymbol%7Bv%7D_%7B%5Cperp%7D%20+%20sin%5Ctheta%5Cboldsymbol%7Bv%7D_%7B%5Ctimes%7D%20%3D%20%28sin%5Ctheta%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20-%20cos%5Ctheta%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E2%29%20%5Cboldsymbol%7Bv%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bu%7D%20%3D%20%5Cboldsymbol%7Bu%7D_%7B%5Cperp%7D%20+%20%5Cboldsymbol%7Bv%7D_%7B%5Cparallel%7D%20%3D%20%28%5Cboldsymbol%7BI%7D%20+%20sin%5Ctheta%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20+%20%281%20-%20cos%5Ctheta%29%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E2%29%20%5Cboldsymbol%7Bv%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7BR%7D%28%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%2C%20%5Ctheta%29%20%3D%20%5Cboldsymbol%7BI%7D%20+%20sin%5Ctheta%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20+%20%281%20-%20cos%5Ctheta%29%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E2) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7B%5Comega%7D%20%3D%20%5Ctheta%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%3D%20%28%5Comega_x%2C%20%5Comega_y%2C%20%5Comega_z%29) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7BR%7D%28%5Cboldsymbol%7B%5Comega%7D%29%20%5Capprox%20%5Cboldsymbol%7BI%7D%20+%20sin%5Ctheta%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20%5Capprox%20%5Cboldsymbol%7BI%7D%20+%20%5Cbegin%7Bbmatrix%7D%20%5Ctheta%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%201%20%26%20-%5Comega_z%20%26%20%5Comega_y%20%5C%5C%20%5Comega_z%20%26%201%20%26%20-%5Comega_x%20%5C%5C%20-%5Comega_y%20%26%20%5Comega_x%20%26%201%20%5Cend%7Bbmatrix%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7BR%7D%28%5Cboldsymbol%7B%5Comega%7D%29%5Cboldsymbol%7Bv%7D%20%5Capprox%20%5Cboldsymbol%7Bv%7D%20+%20%5Cboldsymbol%7B%5Comega%7D%20%5Ctimes%20%5Cboldsymbol%7Bv%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cfrac%7B%5Cpartial%20%5Cboldsymbol%7BRv%7D%7D%7B%5Cpartial%20%5Cboldsymbol%7B%5Comega%7D%5ET%7D%20%3D%20-%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7Bv%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%200%20%26%20z%20%26%20-y%20%5C%5C%20-z%20%26%200%20%26%20x%20%5C%5C%20y%20%26%20-x%20%26%200%20%5Cend%7Bbmatrix%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7BR%7D%28%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%2C%20%5Ctheta%29%20%3D%20%5Clim_%7Bk%5Cto%5Cinfty%7D%20%28%5Cboldsymbol%7BI%7D%20+%20%5Cfrac%7B1%7D%7Bk%7D%5Cbegin%7Bbmatrix%7D%20%5Ctheta%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%29%5Ek%20%3D%20exp%5Cbegin%7Bbmatrix%7D%20%5Comega%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E%7Bk+2%7D%20%3D%20-%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5Ek%2C%20k%20%3E%200) \
![img](https://latex.codecogs.com/svg.latex?%5Cbegin%7Balign*%7D%20exp%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Comega%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20%26%3D%20%5Cboldsymbol%7BI%7D%20+%20%5Ctheta%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20+%20%5Cfrac%7B%5Ctheta%5E2%7D%7B2%7D%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E2%20+%20%5Cfrac%7B%5Ctheta%5E3%7D%7B3%21%7D%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E3%20+%20%5Ccdots%20%5C%5C%20%26%3D%20%5Cboldsymbol%7BI%7D%20+%20%28%5Ctheta%20-%20%5Cfrac%7B%5Ctheta%5E3%7D%7B3%21%7D%20+%20%5Ccdots%29%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20+%20%28%5Cfrac%7B%5Ctheta%5E2%7D%7B2%7D%20-%20%5Cfrac%7B%5Ctheta%5E3%7D%7B4%21%7D%20+%20%5Ccdots%29%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E2%20%5C%5C%20%26%3D%20%5Cboldsymbol%7BI%7D%20+%20sin%5Ctheta%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20+%20%281%20-%20cos%5Ctheta%29%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E2%20%5Cend%7Balign*%7D)

**Unit Quaternions** \
![img](https://latex.codecogs.com/svg.latex?%5Cleft%20%5C%7C%20%5Cboldsymbol%7Bq%7D%20%5Cright%20%5C%7C%20%3D%201) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bq%7D_o%20%3D%20%280%2C%200%2C%200%2C%201%29)
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bq%7D%20%3D%20%28q_x%2C%20q_y%2C%20q_z%2C%20q_w%29%20%3D%20%28x%2C%20y%2C%20z%2C%20w%29%20%3D%20%28%5Cboldsymbol%7Bv%7D%2C%20w%29%20%3D%20%28sin%5Cfrac%7B%5Ctheta%7D%7B2%7D%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%2C%20cos%5Cfrac%7B%5Ctheta%7D%7B2%7D%29) \
![img](https://latex.codecogs.com/svg.latex?%5Cbegin%7Balign*%7D%20%5Cboldsymbol%7BR%7D%28%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%2C%20%5Ctheta%29%20%26%3D%20%5Cboldsymbol%7BI%7D%20+%20sin%5Ctheta%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20+%20%281%20-%20cos%5Ctheta%29%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7B%5Chat%7Bn%7D%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E2%5C%5C%20%26%3D%20%5Cboldsymbol%7BI%7D%20+%202w%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7Bv%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20+%202%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7Bv%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E2%20%5Cend%7Balign*%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7Bv%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%200%20%26%20-z%20%26%20y%5C%5C%20z%20%26%200%20%26%20-x%5C%5C%20-y%20%26%20x%20%26%200%20%5Cend%7Bbmatrix%7D) and ![img](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7Bv%7D%20%5Cend%7Bbmatrix%7D_%7B%5Ctimes%7D%5E2%20%3D%20%5Cbegin%7Bbmatrix%7D%20-y%5E2%20-%20z%5E2%20%26%20xy%20%26%20xz%5C%5C%20xy%20%26%20-x%5E2%20-%20z%5E2%20%26%20yz%5C%5C%20xz%20%26%20yz%20%26%20-x%5E2%20-%20y%5E2%20%5Cend%7Bbmatrix%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7BR%7D%28%5Cboldsymbol%7Bq%7D%29%20%3D%20%5Cbegin%7Bbmatrix%7D%201%20-%202%28y%5E2%20+%20z%5E2%29%20%26%202%28xy%20-%20zw%29%20%26%202%28xz%20+%20yw%29%5C%5C%202%28xy%20+%20zw%29%20%26%201%20-%202%28x%5E2%20+%20z%5E2%29%20%26%202%28yz%20-%20xw%29%5C%5C%202%28xz%20-%20yw%29%20%26%202%28yz%20+%20xw%29%20%26%201%20-%202%28x%5E2%20+%20y%5E2%29%20%5Cend%7Bbmatrix%7D) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bq%7D_2%20%3D%20%5Cboldsymbol%7Bq%7D_0%5Cboldsymbol%7Bq%7D_1%20%3D%20%28%5Cboldsymbol%7Bv%7D_0%20%5Ctimes%20%5Cboldsymbol%7Bv%7D_1%20+%20w_0%5Cboldsymbol%7Bv%7D_1%20+%20w_1%5Cboldsymbol%7Bv%7D_0%2C%20w_0w_1%20-%20%5Cboldsymbol%7Bv%7D_0%20%5Ccdot%20%5Cboldsymbol%7Bv%7D_1%29) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7BR%7D%28%5Cboldsymbol%7Bq%7D_2%29%20%3D%20%5Cboldsymbol%7BR%7D%28%5Cboldsymbol%7Bq%7D_0%29%5Cboldsymbol%7BR%7D%28%5Cboldsymbol%7Bq%7D_1%29) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bq%7D_2%20%3D%20%5Cboldsymbol%7Bq%7D_0%20/%20%5Cboldsymbol%7Bq%7D_1%20%3D%20%5Cboldsymbol%7Bq%7D_0%5Cboldsymbol%7Bq%7D_1%5E%7B-1%7D%20%3D%20%28%5Cboldsymbol%7Bv%7D_0%20%5Ctimes%20%5Cboldsymbol%7Bv%7D_1%20+%20w_0%5Cboldsymbol%7Bv%7D_1%20-%20w_1%5Cboldsymbol%7Bv%7D_0%2C%20-w_0w_1%20-%20%5Cboldsymbol%7Bv%7D_0%20%5Ccdot%20%5Cboldsymbol%7Bv%7D_1%29) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bq%7D_2%20%3D%20%5Cboldsymbol%7Bq%7D_%7Br%7D%5E%5Calpha%20%5Cboldsymbol%7Bq%7D_0) \
![img](https://latex.codecogs.com/svg.latex?%5Cboldsymbol%7Bq%7D_2%20%3D%20%5Cfrac%7Bsin%281%20-%20%5Calpha%29%5Ctheta%7D%7Bsin%5Ctheta%7D%20%5Cboldsymbol%7Bq%7D_%7B0%7D%20+%20%5Cfrac%7Bsin%5Calpha%5Ctheta%7D%7Bsin%5Ctheta%7D%20%5Cboldsymbol%7Bq%7D_1) \
where ![img](https://latex.codecogs.com/svg.latex?%5Ctheta%20%3D%20cos%5E%7B-1%7D%28%5Cboldsymbol%7Bq%7D_%7B0%7D%20%5Ccdot%20%5Cboldsymbol%7Bq%7D_1%29)

## 3D to 2D Projections

**Orthography & Para-Perspective** \

**Perspective** \

**Camera Intrinsics** \

**Fonal Lengths** \

**Camera Matrix** \

**Projective Depth (plane-plus-parallex)** \

**Mapping (camera-to-camera)** \

**Object-Centered Projection** \

## Lens Distortion

![img](http://latex.codecogs.com/gif.latex?x_c%20%3D%20%5Cfrac%7B%5Cboldsymbol%7Br%7D_x%20%5Ccdot%20%5Cboldsymbol%7Bp%7D%20+%20t_x%7D%7B%5Cboldsymbol%7Br%7D_z%20%5Ccdot%20%5Cboldsymbol%7Bp%7D%20+%20t_z%7D) \
![img](http://latex.codecogs.com/gif.latex?y_c%20%3D%20%5Cfrac%7B%5Cboldsymbol%7Br%7D_y%20%5Ccdot%20%5Cboldsymbol%7Bp%7D%20+%20t_y%7D%7B%5Cboldsymbol%7Br%7D_z%20%5Ccdot%20%5Cboldsymbol%7Bp%7D%20+%20t_z%7D) \
![img](http://latex.codecogs.com/gif.latex?%5Chat%7Bx%7D_c%20%3D%20x_c%281%20+%20%5Ckappa_1r_c%5E2%20+%20%5Ckappa_2r_c%5E4%29) \
![img](http://latex.codecogs.com/gif.latex?%5Chat%7By%7D_c%20%3D%20y_c%281%20+%20%5Ckappa_1r_c%5E2%20+%20%5Ckappa_2r_c%5E4%29) \
where ![img](http://latex.codecogs.com/gif.latex?r_c%5E2%20%3D%20x_c%5E2%20+%20y_c%5E2) \
![img](http://latex.codecogs.com/gif.latex?x_s%20%3D%20fx%27_c%20+%20c_x) \
![img](http://latex.codecogs.com/gif.latex?y_s%20%3D%20fy%27_c%20+%20c_y)

# Photometric Image Formation

## Lighting

## Reflectance & Shading

## Optics

# Digital Camera

## Sampling & Aliasing

## Color

## Compression
