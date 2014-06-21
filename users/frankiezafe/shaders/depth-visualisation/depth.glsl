uniform sampler2D bgl_DepthTexture;

void main(void) {
    vec4 dc = texture2D( bgl_DepthTexture, gl_TexCoord[0].st );
    float depth = ( 1.0 - dc.r ) * 8.0;
    // 1 -> blanc
    // 0 -> noir
    gl_FragColor = vec4( depth, depth, depth, 1.0);

}