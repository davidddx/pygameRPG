<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.10.2" name="Test" tilewidth="32" tileheight="32" tilecount="29" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteDown.png"/>
 </tile>
 <tile id="1">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteDownLeft.png"/>
 </tile>
 <tile id="2">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteDownRight.png"/>
 </tile>
 <tile id="3">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteLeft.png"/>
 </tile>
 <tile id="4">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteMiddle.png"/>
 </tile>
 <tile id="5">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteRight.png"/>
 </tile>
 <tile id="6">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteUp.png"/>
 </tile>
 <tile id="7">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteUpLeft.png"/>
 </tile>
 <tile id="8">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteUpRight.png"/>
 </tile>
 <tile id="9">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/GrassSprite.png"/>
 </tile>
 <tile id="11">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteCornerBottomRight.png"/>
 </tile>
 <tile id="12">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteCornerTopLeft.png"/>
 </tile>
 <tile id="13">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteCornerTopRight.png"/>
 </tile>
 <tile id="10">
  <properties>
   <property name="collision" type="bool" value="false"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/DirtSpriteCornerBottomLeft.png"/>
 </tile>
 <tile id="14">
  <properties>
   <property name="collision" type="bool" value="true"/>
  </properties>
  <image width="32" height="32" source="../../../images/test/Fence.png"/>
 </tile>
 <tile id="15">
  <image width="32" height="32" source="../../../images/test/FenceLeftEnd.png"/>
 </tile>
 <tile id="16">
  <image width="32" height="32" source="../../../images/test/FenceRightEnd,png.png"/>
 </tile>
 <tile id="17">
  <image width="32" height="32" source="../../../images/test/FenceBottomLeft.png"/>
 </tile>
 <tile id="18">
  <image width="32" height="32" source="../../../images/test/FenceBottomRight.png"/>
 </tile>
 <tile id="19">
  <image width="32" height="32" source="../../../images/test/FenceTopLeft.png"/>
 </tile>
 <tile id="20">
  <image width="32" height="32" source="../../../images/test/FenceTopRight.png"/>
 </tile>
 <tile id="21">
  <image width="32" height="32" source="../../../images/test/FenceVertical.png"/>
 </tile>
 <tile id="22">
  <image width="32" height="32" source="../../../images/test/FenceHorizontal2.png"/>
 </tile>
 <tile id="23">
  <image width="32" height="32" source="../../../images/test/FenceVertical2.png"/>
 </tile>
 <tile id="24">
  <image width="32" height="32" source="../../../images/test/FenceBottomLeft2.png"/>
 </tile>
 <tile id="25">
  <image width="32" height="32" source="../../../images/test/FenceBottomRight2.png"/>
 </tile>
 <tile id="26">
  <image width="32" height="32" source="../../../images/test/FenceTopLeft2.png"/>
 </tile>
 <tile id="27">
  <image width="32" height="32" source="../../../images/test/FenceTopRight2.png"/>
 </tile>
 <tile id="28">
  <image width="32" height="32" source="../../../images/test/Nothing.png"/>
 </tile>
 <wangsets>
  <wangset name="DirtGrass" type="corner" tile="-1">
   <wangcolor name="Dirt" color="#ff0000" tile="-1" probability="1"/>
   <wangcolor name="grass" color="#00ff00" tile="-1" probability="1"/>
   <wangtile tileid="0" wangid="0,1,0,2,0,2,0,1"/>
   <wangtile tileid="1" wangid="0,1,0,2,0,2,0,2"/>
   <wangtile tileid="2" wangid="0,2,0,2,0,2,0,1"/>
   <wangtile tileid="3" wangid="0,1,0,1,0,2,0,2"/>
   <wangtile tileid="4" wangid="0,1,0,1,0,1,0,1"/>
   <wangtile tileid="5" wangid="0,2,0,2,0,1,0,1"/>
   <wangtile tileid="6" wangid="0,2,0,1,0,1,0,2"/>
   <wangtile tileid="7" wangid="0,2,0,1,0,2,0,2"/>
   <wangtile tileid="8" wangid="0,2,0,2,0,1,0,2"/>
   <wangtile tileid="9" wangid="0,2,0,2,0,2,0,2"/>
   <wangtile tileid="10" wangid="0,1,0,1,0,2,0,1"/>
   <wangtile tileid="11" wangid="0,1,0,2,0,1,0,1"/>
   <wangtile tileid="12" wangid="0,1,0,1,0,1,0,2"/>
   <wangtile tileid="13" wangid="0,2,0,1,0,1,0,1"/>
  </wangset>
  <wangset name="Fence" type="corner" tile="-1">
   <wangcolor name="Fence" color="#ff0000" tile="-1" probability="1"/>
   <wangcolor name="Dirt" color="#00ff00" tile="-1" probability="1"/>
   <wangtile tileid="4" wangid="0,2,0,2,0,2,0,2"/>
   <wangtile tileid="14" wangid="0,2,0,1,0,1,0,2"/>
   <wangtile tileid="17" wangid="0,1,0,2,0,2,0,2"/>
   <wangtile tileid="18" wangid="0,2,0,2,0,2,0,1"/>
   <wangtile tileid="19" wangid="0,2,0,1,0,2,0,2"/>
   <wangtile tileid="20" wangid="0,1,0,1,0,2,0,1"/>
   <wangtile tileid="21" wangid="0,1,0,1,0,2,0,2"/>
   <wangtile tileid="22" wangid="0,1,0,2,0,2,0,1"/>
   <wangtile tileid="23" wangid="0,2,0,2,0,1,0,1"/>
   <wangtile tileid="24" wangid="0,1,0,2,0,2,0,2"/>
   <wangtile tileid="25" wangid="0,1,0,1,0,1,0,2"/>
   <wangtile tileid="26" wangid="0,1,0,2,0,1,0,1"/>
   <wangtile tileid="27" wangid="0,1,0,1,0,2,0,1"/>
  </wangset>
 </wangsets>
</tileset>
