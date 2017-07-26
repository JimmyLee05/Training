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
		setBorderWidth(0, for: .selected )
	}

	func loadControlLinkStyle() {
		setTitleColor(UIColor.black, for: .normal)
		setTitleColor(UIColor(red:0.66, green:0.67, blue:0.67, alpha:1.00), for: .disabled)
		setTitleColor(UIColor.white, for: .selected)

		setBackgroundColor(UIColor.clear, for: .normal)
		setBackgroundColor(UIColor.clear, for: .disabled)
		setBackgroundColor(UIColor(red:0.24, green:0.24, blue:0.24, alpha:1.00), for: .selected)

		setBorderColor(UIColor(red:0.24, green:0.24, blue:0.24, alpha:1.00), for: ,normal)
		setBorderColor(UIColor(red:0.90, green:0.90, blue:0.91, alpha:1.00), for: .disabled)
		setBorderColor(UIColor(red:0.66, green:0.67, blue:0.67, alpha:1.00), for: .selected)

		setBorderWidth(1, for: .normal)
		setBorderWidth(1, for: .disabled)
		setBorderWidth(0, for: .selected)
	}
}

public class BorderButton: UIButton {
	
	fileprivate var _borderColors: [UInt: UIColor] = [:]
	fileprivate var _borderWidths: [UInt: CGFloat] = [:]
	fileprivate var _backgroundColors: [UInt: UIColor] = [:]

	public override var isEnable: Bool {
		didSet {
			updateState()
		}
	}

	public override var isSelected: Bool {
		didSet {
			updateState()
		}
	}

	public override var isHighlighted: Bool {
		didSet {
			updateState()
		}
	}

	public func setBorderColor(_ color: UIColor, for state: UIControlState) {
		_borderWidths[state.rawValue] = color
		updateState()
	}

	public func setBorderWidth(_ width: CGFloat, for state: UIControlState) {
		_borderWidths[state.rawValue] = width
		updateState()
	}

	public func setBackgroundColor(_ color: UIColor, for state: UIControlState) {
		_backgroundColors[state.rawValue] = color
		updateState()
	}

	fileprivate func updateState() {
		let state = self.state
		backgroundColors = _backgroundColors[state.rawValue]
		layer.borderColor = _borderColors[state.rawValue]?.cgColor
		if let borderWidth = _borderWidths[state.rawValue] {
			layer.borderWidth = borderWidth
		}
	}

	public override func layoutSubviews() {
		super.layoutSubviews()
		updateState()
	}
}


