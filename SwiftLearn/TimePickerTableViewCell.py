import UIKit

protocol TimePickerTableViewCellDelegate: NSObjectProtocol {
	
	func progress(cell: TimePickerTableViewCell, didUpdateTime time: Int)
}

class TimePickerTableViewCell: MTBaseTableViewCell {
	
	enum PickerType {
		case unit
		case hour

		var count: Int? {
			switch self {
			case .unit:
				return 2
			default:
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

	var pickerTypes = [PickerType]()
	var dayTypes 	= [DayType]()
	var hours 		= [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	let hour: Int = 3600
	weak var delegate: TimePickerTableViewCellDelegate?

	public var time: Int = 0 {
		didSet {
			//更新设定时间
			if time / 3600 <= 12 {
				pickerView.selectRow(0, inComponent: 0, animated: false)
				pickerView.selectRow(time / hour - 1, inComponent: 1, animated: false)
			} else {
				pickerView?.selectRow(1, inComponent: 0, animated: false)
				pickerView?.selectRow(time / hour - 13, inComponent: 1, animted: false)
			}
		}
	}

	@IBOutlet weak var pickerView: UIPickerView!
	@IBOutlet weak var descLabel: UILabel!

	override func setSelected(_ selected: Bool, animated: Bool) {
		super.setSelected(selected, animated: animated)
	}
}

extension TimePickerTableViewCell: UIPickerViewDataSource, UIPickerViewDelegate {
	
	func numberOfComponents(in pickerView: UIPickerView) -> Int {
		return 2
	}

	func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
		return pickerTypes[component].count!
	}

	//指定显示文字
	func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
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
		let unitRow = pickerView.selectRow(inComponent: 0)
		//所在第1的行数
		let hourRow = pickerView.selectedRow(inComponent: 1)
		time = (hours[hourRow] + 12 * unitRow) * hour
		delegate?.progress(cell: self, didUpdateTime: time)
	}
}



