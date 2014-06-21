uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;
uniform float percentage;
uniform float timer;
uniform float xmin;
uniform float xmax;
uniform float ymin;
uniform float ymax;

void main(void) {
    
    // using depth
    vec4 dc = texture2D(bgl_DepthTexture, gl_TexCoord[0].st);
    
    float x = gl_TexCoord[0].st.x;
    float y = gl_TexCoord[0].st.y;
    if ( 
        // x >= xmin && x <= xmax &&
        y >= ymin && y <= ymax
        )
    {
    // NOISE
        float noiseR = (fract(sin(dot(gl_TexCoord[0].st ,vec2(12.9898,78.233)+timer)) * 43758.5453));
	   float noiseG =     (fract(sin(dot(gl_TexCoord[0].st ,vec2(12.9898,78.233)+timer*2)) * 43758.5453)); 
	   float noiseB =     (fract(sin(dot(gl_TexCoord[0].st ,vec2(12.9898,78.233)+timer*3)) * 43758.5453));
        
        vec4 noise = vec4( noiseR, noiseG, noiseB, 1.0 );
        float range = ( ymax - ymin ) * 0.5;
        range = ( y - ( ymin + range ) ) / range;
        if ( range < 0 ) { range *= -1; }
        gl_FragColor = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st) + ( noise * percentage );

    // INVERT COLORS
    /*
    	vec4 invert = 1.0 - texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);
    	vec4 color = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);
    	gl_FragColor = mix(color, invert, percentage);
    	gl_FragColor.a = 1.0;
    */
    } else {
        gl_FragColor = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);
    }
}