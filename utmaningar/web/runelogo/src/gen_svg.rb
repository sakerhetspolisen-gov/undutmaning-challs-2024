require 'nokogiri'

def generate_svg(str, tmpl)
  begin
    svg = Nokogiri::XML(tmpl,nil,nil,2)
  rescue => error
    STDERR.puts tmpl
    STDERR.puts error.message
    return 400
  end
  return 400 unless svg.errors.empty? 

  style = svg.at_css("style")
  font = "Noto Sans Runic"
  font_el = "@import url('https://fonts.googleapis.com/css?family=#{font.gsub(' ', '+')}');\n"
  style.add_child(Nokogiri::XML::Text.new(font_el, svg)) if style
  0.upto(4) do |i|
    colsel = ".randcol"+i.to_s
    col = '#' + rand(0xffffff).to_s(16)
    svg.css(colsel).each do |c|
      c["fill"] = col
    end
  end
  txt = svg.at_css("#content")
  txt.content = str if txt
  svg.css(".content").each do |con|
    con.content = str
  end
  txt["style"] = txt["style"].to_s + "font-family:#{font}"
  txt["font-size"] = "2em" if txt
  clickstr = '<script>document.getElementById("logo").setAttribute("onclick","window.location.reload();");</script>'
  '<div id="logo">' + svg.to_xml + '</div>' + clickstr
end

def generate_front()
  tmpl = %q(
<svg width="100%" viewBox="0 0 750 1000" xmlns="http://www.w3.org/2000/svg" >
  <defs id="defs">
    <radialGradient
    id="gradient1"
    gradientUnits="userSpaceOnUse"
    cx="100"
    cy="100"
    r="100"
    fx="100"
    fy="100">
    <stop offset="0%" stop-color="darkblue" />
    <stop offset="50%" stop-color="skyblue" />
    <stop offset="100%" stop-color="darkblue" />
    <animate id="a0" attributeName="r" from="10%" to="95%" dur="2s" begin="10" repeatCount="indefinite" />
  </radialGradient>
    <radialGradient id="bgGradient">
      <stop offset="10%" stop-color="gold" />
      <stop offset="95%" stop-color="green" />
      <animate id="a1" attributeName="r" from="10%" to="95%" dur="2s" begin="0;a2.end" />
      <animate id="a2" attributeName="r" from="95%" to="10%" dur="2s" begin="a1.end"  />
    </radialGradient>
  </defs>
<rect width="100%" height="100%" fill="url(#gradient1)"/>
<svg x="50" y="50" width="500">
<style type="text/css">
  @import url('https://fonts.googleapis.com/css?family=Sacramento');
</style>
  <g id="contentgroup" style="font-family:Sacramento;font-size:24px;fill:yellow;">
<svg>
  <text x="0" y="20">Your own</text>
  </svg>
<svg x="80">
  <svg>
  <text x="10" y="20">a
  <animate
    id="c0"
    attributeName="y"
    values="15;25;20"
    dur="0.3s"
    begin="a0.begin;c7.end-0.2">
  </animate>
  </text>
</svg>
<svg>
  <text x="20" y="20">n
  <animate
    id="c1"
    attributeName="y"
    values="15;25;20"
    dur="0.3s"
    begin="c0.end-0.2">
  </animate>
</text>
</svg>
<svg>
  <text x="30" y="20">i
  <animate
    id="c2"
    attributeName="y"
    values="15;25;20"
    dur="0.3s"
    begin="c1.end-0.2">
  </animate>
</text>
</svg>
<svg>
  <text x="35" y="20">m
  <animate
    id="c3"
    attributeName="y"
    values="15;25;20"
    dur="0.3s"
    begin="c2.end-0.2">
  </animate>
</text>
</svg>
<svg>
  <text x="50" y="20">a
  <animate
    id="c4"
    attributeName="y"
    values="15;25;20"
    dur="0.3s"
    begin="c3.end-0.2">
  </animate>
</text>
</svg>
<svg>
  <text x="60" y="20">t
  <animate
    id="c5"
    attributeName="y"
    values="15;25;20"
    dur="0.3s"
    begin="c4.end-0.2">
  </animate>
</text>
</svg>
<svg>
  <text x="68" y="20">e
  <animate
    id="c6"
    attributeName="y"
    values="15;25;20"
    dur="0.3s"
    begin="c5.end-0.2">
  </animate>
</text>
</svg>
<svg>
  <text x="77" y="20">d
  <animate
    id="c7"
    attributeName="y"
    values="15;25;20"
    dur="0.3s"
    begin="c6.end-0.2">
  </animate>
</text>
</svg>
<svg>
  <text x="95" y="20">RUNIC logo!!</text>
  </svg>
  </g>
</svg>
</svg>

  <svg x="100" y="200">
  <svg>
  <style>
    #btn {
       border-radius: 5px;
       background: orange;
       border: 2px solid red;
       text-align: center;
       }
    #wire {
       stroke-dashoffset:69.74px;
       stroke-dasharray:69.74px;
       stroke:red;
       stroke-width:2px;
       fill:none;
}
  </style>
  <foreignObject x="10" y="10" width="90%" height="50">
      <div xmlns="http://www.w3.org/1999/xhtml">
      <form id="setstr" action="/setstring" method="post">
      <input name="str"></input>
      </form>
          </div>
  </foreignObject>
  <svg x="20" y ="100">
  <g rotate(10,60,125) >
  <foreignObject width="100" height="100">
    <div id="btn" onclick="document.getElementById('setstr').submit()">Set string!</div>
  </foreignObject>
          <animateTransform
    attributeName="transform"
    type="rotate"
    values="-10 60 125;10 60 125;-10 60 125"
    begin="a0.begin"
    dur="2s"
    repeatCount="indefinite" />

  </g>
  </svg>
      <path id="wire" d="M35,35 C15,50 20,60 30,65 40,70 45,75 40,90" >
       <!-- Curved path growth animation -->
        <animate
           attributeName="stroke-dashoffset"
           begin="a0.begin"
           dur="3s"
           values="69.74;0"
           calcMode="linear"
           fill="freeze"
           restart="whenNotActive" 
           repeatCount="indefinite" >
        </animate>
    </path>
    <!-- Cursor -->
    <polygon points="-5,-5 5,0 -5,5 -3,0" fill="red">
          <!-- Animating cursor movement along a curved path -->
        <animateMotion begin="a0.begin" dur="3s" repeatCount="indefinite" calcMode="linear" rotate="auto" fill="freeze">
            <mpath xlink:href="#wire" />
        </animateMotion>
    </polygon>
</svg>
</svg>
</svg>
</svg>
)
  front = Nokogiri::XML(tmpl)
  front.to_xml
end
