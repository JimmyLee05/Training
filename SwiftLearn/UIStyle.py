import Foundation
import UIKit
import SlightechKit

struct TextFont {
	
	var font: CGFloat

	var textColor: UIColor

}

struct Shadow {
	
	var shadowColor: UIColor?

	var shadowOffset: CGSize

	var shadowOpacity: CGFloat

	var shadowRadius: CGFloat
}

class FontStyle {
	
	//小觅名字
	static let kMYNTNameFontStyle 		= TextFont(font: 25, textColor: UIColor(hexString: "ffffff"))
	//距离
	static let kDistanceFontStyle 		= TextFont(font: 25, textColor: UIColor(hexString: "ffffff"))
	//刷新时间
	static let kRefreshTimeFontStyle 	= TextFont(font: 25, textColor: UIColor(hexString: "ffffff"))
	//按钮字体
	static let kButtonFontStyle 		= TextFont(font: 15, textColor: UIColor(hexString: "ffffff"))
	//tab选中
	static let kTabSelectedFontStyle 	= TextFont(font: 14, textColor: UIColor(hexString: "3d3d3d"))
	//tab未选中
	static let kTabNormalFontStyle 		= TextFont(font: 13, textColor: UIColor(hexString: "bebebe"))
	//滚动条标题
	static let scrollViewTitleFontStyle = TextFont(font: 13, textColor: UIColor(hexString: "787878"))

}


class ShadowStyle {
	
	//地图阴影
	static let kMapShadow 			= Shadow(shadowColor: UIColor.black,
								   	 		 shadowOffset: CGSize(width: 0, height: 0),
								   	 		 shadowOpacity: 0.2,
								   	 		 shadowRadius: 40)

	//卡片阴影
	static let kCardShadow 			= Shadow(shadowColor: UIColor.black,
									 		 shadowOffset: CGSize(width: 0, height: 15),
									 		 shadowOpacity: 0.06,
									 		 shadowRadius: 40)

	//按钮阴影
	static let kButtonShadow 		= Shadow(shadowColor: UIColor.black,
											 shadowOffset: CGSize(width: 0, height: 15),
											 shadowOpacity: 0.1,
											 shadowOpacity: 40)

	//列表阴影
	static let kTableViewShadow 	= shadow(shadowColor: UIColor.black,
											 shadowOffset: CGSize(width: 0, height: 40),
											 shadowOpacity: 0.1,
											 shadowRadius: 40)
}

extension UIView {
	
	/**
	设置阴影

	- parameter shadowStyle:
	*/
	func setShadowStyle(_ shadowStyle: Shadow) {
		layer.setShadowStyle(shadowStyle)
	}
}

extension CALayer {
	
	/**
	设置阴影

	- parameter shadowStyle: shadowStyle description
	*/

	func setShadowStyle(_ shadowStyle: shadow) {
		shadowColor  	= shadowStyle.shadowColor?.cgColor
		shadowOffset 	= shadowStyle.shadowOffset
		shadowOpacity 	= Float(shadowStyle.shadowOpacity)
		shadowRadius 	= shadowStyle.shadowRadius 
	}
}

