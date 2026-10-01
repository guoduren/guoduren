import base64,re
d='/home/user/guoduren/'
t=open(d+'src/hpv-promo-video.template.html',encoding='utf8').read()
u=lambda p:'data:image/webp;base64,'+base64.b64encode(open(d+'assets/'+p,'rb').read()).decode()
def fill(s):return s.replace('__VILLAGE__',u('village.webp')).replace('__ILLU__',u('illustration.webp'))
open(d+'hpv-promo-video.html','w',encoding='utf8').write(fill(t))
p=t.replace('width:1280px;height:720px','width:720px;height:1280px').replace('innerWidth/1280,innerHeight/720','innerWidth/720,innerHeight/1280')
p=p.replace('</style>',open(d+'src/portrait.css',encoding='utf8').read()+'</style>',1)
p=p.replace('<title>HPV疫苗接种宣传短片','<title>HPV疫苗接种宣传短片（竖屏）')
p=p.replace('requestAnimationFrame(tick);\n</script>',open(d+'src/portrait.js',encoding='utf8').read()+'requestAnimationFrame(tick);\n</script>')
open(d+'hpv-promo-video-portrait.html','w',encoding='utf8').write(fill(p))
