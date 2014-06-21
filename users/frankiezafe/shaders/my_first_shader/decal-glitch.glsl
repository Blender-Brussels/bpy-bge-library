uniform sampler2D bgl_RenderedTexture;
uniform float glitchdecal;
uniform float glitchdecalstart;
uniform float glitchdecalend;

void main(void) {
    
    float x = gl_TexCoord[0].st.x;
    float y = gl_TexCoord[0].st.y;
    
    if ( y > glitchdecalstart && y < glitchdecalend ) {
        
        float decalx = x + glitchdecal;
        if ( decalx < 0 ) { decalx = 0; }
        else if ( decalx > 1 ) { decalx = 1; }
        
        gl_FragColor = texture2D(bgl_RenderedTexture, vec2( decalx, y ) );
                
    } else {
    
        gl_FragColor = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);
    
    }
    
}