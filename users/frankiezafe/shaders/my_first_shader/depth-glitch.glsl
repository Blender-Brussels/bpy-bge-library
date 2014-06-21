uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;
uniform float timer;
uniform float glitchd;
uniform float glitchspan;

vec3 convertRGBtoHSV(vec3 rgbColor) {
    float r = rgbColor[0];
    float g = rgbColor[1];
    float b = rgbColor[2];
    float colorMax = max(max(r,g), b);
    float colorMin = min(min(r,g), b);
    float delta = colorMax - colorMin;
    float h = 0.0;
    float s = 0.0;
    float v = colorMax;
    vec3 hsv = vec3(0.0);
    if (colorMax != 0.0) {
      s = (colorMax - colorMin ) / colorMax;
    }
    if (delta != 0.0) {
        if (r == colorMax) {
            h = (g - b) / delta;
        } else if (g == colorMax) {        
            h = 2.0 + (b - r) / delta;
        } else {    
            h = 4.0 + (r - g) / delta;
        }
        h *= 60.0;
        if (h < 0.0) {
            h += 360.0;
        }
    }
    hsv[0] = h;
    hsv[1] = s;
    hsv[2] = v;
    return hsv;
}

void main(void) {
    
    // using depth
    vec4 dc = texture2D(bgl_DepthTexture, gl_TexCoord[0].st);
    float depth = ( 1.000 - ( (dc.r + dc.g + dc.b) / 3.0 ) ) * 16.000;
    
    // validation
    // vec4 rgba = vec4( depth, depth, depth, 1.0);
    // gl_FragColor = rgba;
    
    vec4 rgba = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);
    
    // noise on black zones
    vec3 hsv = convertRGBtoHSV( (vec3) rgba );
    if ( hsv[ 2 ] < 0.2 ) {
        float noiseAmount = (fract(sin(dot(gl_TexCoord[0].st ,vec2(12.9898,78.233)+timer)) * 43758.5453)) * 0.6;
        vec4 noiseColor = vec4( noiseAmount, noiseAmount, noiseAmount, 1.0 );
        rgba += ( noiseColor * noiseAmount * ( 1 - ( hsv[ 2 ] / 0.2 ) ) );
    }
    
    // red laser
    if ( depth > 0 && depth > glitchd - glitchspan && depth < glitchd + glitchspan ) {
        float d = ( ( depth - glitchd ) / glitchspan );
        if ( d < 0 ) {
            d *= -1;
        }
        d = 1-d;
        float redamount = (fract(sin(dot(gl_TexCoord[0].st ,vec2(12.9898,78.233)+timer)) * 43758.5453)) * d;
        // vec4 noiseColor = vec4( noiseAmount, 0.5, 0.5, 1.0 );
        rgba[ 0 ] += redamount;
        
    } else if ( depth == 0 || depth == 0.1 ) {
        
        rgba = vec4( 0, 0, 0, 1.0);
        /*
        // get symetric color
        float r = (fract(sin(dot(gl_TexCoord[0].st ,vec2(12.9898,78.233)+timer)) * 43758.5453)) * 1000;
        if ( r < 250 ) {
            rgba = texture2D(bgl_RenderedTexture, vec2( 1 - gl_TexCoord[0].st.x, gl_TexCoord[0].st.y * 0.5) );
        } else if ( r < 500 ) {
            rgba = texture2D(bgl_RenderedTexture, vec2( 1 - gl_TexCoord[0].st.x, 1 - gl_TexCoord[0].st.y ) );
        } else if ( r < 750 ) {
            rgba = texture2D(bgl_RenderedTexture, vec2( gl_TexCoord[0].st.x, 1 - gl_TexCoord[0].st.y ) );
        } else {
            rgba = vec4( 0, 0, 0, 1.0);
        }
        */
        
    }
    
    
    gl_FragColor = rgba;
    
}