import UIKit
import MYNTKit

class PickerDialogView: DialogBaseView {
	
	enum PickerType {
		case unit
		case hour

		var count: Int? {
			switch self {
			case .unit:
				return 2
			case .hour:
				return 12
			}
		}
	}

	enum DayType {
		case am
		case pm

		var dayString: String? {
			switch self {
			case .am:
				return "上午"
			case .pm:
				return "下午"
			}
		}
	}

	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var pickerView: UIPickerView!
	@IBOutlet weak var okButton: GradientButton!
	@IBOutlet weak var okHeightConstraint: NSLayoutConstraint!

	var pickerTypes = [PickerType]()
	var dayTypes 	= [DayType]()

	var hours = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	let hour: Int = 3600

	var time: Int = 0 {
		didSet {
			//更新时间
			if time / 3600 <= 12 {
				pickerView?.selectRow(0, inComponent: 0, animated: false)
				pickerView?.selectRow(time / hour - 1, inComponent: 1, animated: false)
			} else {
				pickerView?.selectRow(1, inComponent: 0, animated: false)
				pickerView?.selectRow(time / hour - 13, inComponent: 1, animated: false)
			}
		}
	}

	override func awakeFromNib() {
		okButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)

		pickerTypes = [.unit, .hour]
		dayTypes 	= [.am, .pm]

		pickerView.delegate 	= self
		pickerView.dataSource 	= self
	}
}

extension PickerDialogView: UIPickerViewDataSource, UIPickerViewDelegate {
	
	func numberOfComponents(in pickerView: UIPickerView) -> Int {
		return 2
	}

	func pickerView(_ pickerView: UIPickerView, numberOfComponents comonent: Int) -> Int {
		return pickerTypes[component].count!
	}

	//指定显示文字
	func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent: Int) -> String? {
		let item = pickerTypes[component]
		switch item {
		case .unit:
			return dayTypes[row].dayString
		case .hour:
			return "\(hours[row])"
		}
	}

	//选中指定行列
	func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
		//所在第0列的行数
		let unitRow = pickerView.selectedRow(inComponent: 0)
		//所在第1的行数
		let hourRow = pickerView.selectedRow(inComponent: 1)
		time = (hours[hourRow] + 12 * unitRow) * hour
	}
}

