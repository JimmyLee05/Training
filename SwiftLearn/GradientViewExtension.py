import Foundation

extension GradientView {
	
	//加载遮罩
	func loadTableViewMaskStyle() {
		//高度
		constraint.first?.constant = 140
		//颜色样式
		direction 		= top2bottom
		locations 		= [0, 1]
		colors 			= [UIColor(red: 1, green: 1, blue: 1, alpha: 0),
								UIColor(red: 1, green: 1, blue: 1, alpha: 1)]
	}
}