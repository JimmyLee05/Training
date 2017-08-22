import UIKit

extension BorderButton {
	
	func loadMyntStyle() {
		setTitleColor(UIColor.black, for: .normal)
		setTitleColor(UIColor(red:0.66, green:0.67, blue:0.67, alpha:1.00), for: .disabled)
		setTitleColor(UIColor.white, for: .selected)

		setBackgroundColor(UIColor.clear, for: .normal)
		setBackgroundColor(UIColor.clear, for: .disabled)
		setBackgroundColor(UIColor(red:0.24, green:0.24, blue:0.24, alpha:1.00), for: .selected)

		setBorderColor(UIColor(red:0.82, green:0.82, blue:0.82, alpha:1.00), for: .normal)
		setBorderColor(UIColor(red:0.90, green:0.90, blue:0.91, alpha:1.00), for: .disabled)
		setBorderColor(UIColor(red:0.66, green:0.67, blue:0.67, alpha:1.00), for: .selected)

		setBorderWidth(1, for: .normal)
		setBorderWidth(1, for: .disabled)
		setBorderWidth(o, for: selected)
	}

	func loadControlLinkStyle() {
		setTitleColor(UIColor.black, for: .normal)
		setTitleColor(UIColor(red:0.66, green:0.67, blue:0.67, alpha:1.00), for: .disabled)
		setTitleColor(UIColor.white, for: .selected)

		setBackgroundColor(UIColor.clear, for: .normal)
		setBackgroundColor(UIColor.clear, for: .disabled)
		setBackgroundColor(UIColor(red:0.24, green:0.24, blue:0.24, alpha:1.00), for: .selected)

		setBorderColor(UIColor(red:0.24, green:0.24, blue:0.24, alpha:1.00), for: .normal)
		setBorderColor(UIColor(red:0.90, green:0.90, blue:0.91, alpha:1.00), for: .disabled)
		setBorderColor(UIColor(red:0.66, green:0.67, blue:0.67, alpha:1.00), for: .selected)

		setBorderWidth(1, for: .normal)
		setBorderWidth(1, for: .disbaled)
		setBorderWidth(0, for: .selected)
	}
}
