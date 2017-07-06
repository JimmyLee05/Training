import UIKit

class DebugConfigViewController: BaseViewController {
	
	enum ConfigType: Int {
		case sensitivityLow
		case sensitivityMiddle
		case sensitivityHigh
		case frequencyOff
		case frequencyFast
		case frequencyMiddle
		case frequencySlow

		static var all: [ConfigType] = [.sensitivityLow,
										.sensitivityMiddle,
										.sensitivityHigh,
										.frequencyOff,
										.frequencyFast,
										.frequencyMiddle,
										.frequencySlow]
		var name: String {
			switch self {
				case .sensitivityLow:
					return "灵敏度 - 低"
				case .sensitivityMiddle:
					return "灵敏度 - 中"
				case .sensitivityHigh:
					return "灵敏度 - 高"
				case .frequencyOff:
					return "定位频率 - 关"
				case .frequrecyFast:
					return "定位频率 - 快"
				case .frequencyMiddle:
					return "定位频率 - 中"
				case .frequencySlow:
					return "定位频率 - 慢"
			}
		}

		var value: Int {
			switch self {
			case .sensitivityLow:
				return MyntParamConfig.shared.getAlarmDelay(sensitivity: .low)
			case .sensitivityMiddle:
				return MyntParamConfig.shared.getAlarmDelay(sensitivity: .middle)
			case .sensitivityHigt:
				return MyntParamConfig.shared.getAlarmDelay(sensitivity: .higt)
			case .frequencyOff:
				return MyntParamConfig.shared.getLoactionFrequency(frequency: .off)
			case .frequencyFast:
				return MyntParamConfig.shared.getLoactionFrequency(frequency: .fast)
			case .frequencyMiddle:
				return MyntParamConfig.shared.getLoactionFrequency(frequency: .medium)
			case .frequencySlow:
				return MyntParamConfig.shared.getLoactionFrequency(frequency: .slow)
			}
		}
	}

	@IBOutlet weak var tableView: UITableView!

	override func viewDidLoad() {
		super.viewDidLoad()

		tableView.register(with: DebugConfigTableViewCell.self)
		tableView.delegate = self
		tableView.dataSource = self
		tableView.estimatedRowHeight = 45
		tableView.rowHeight = UITableViewAutomaticDimension
		tableView.tableFooterView = UIView()
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	@IBAction func didClickSaveButton(_ sender: UIButton) {

	}

}

extension DebugConfigViewController: UITableViewDelegate, UITableViewDataSource {
	
	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return ConfigType.all.count
	}

	func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCell(cell: DebugConfigTableViewCell.self, for: indexPath)
		cell?.type = ConfigType.all[indexPath.row]
		cell?.nameLabel.text = ConfigType.all[indexPath.row].name
		cell?.valueTextField.text = "\(ConfigType.all[indexPath.row].value)"
		cell?.doneHandler = {type, value in
			switch type {
			case .sensitivityLow:
				MyntParamConfig.shared.setAlarmDelay(sensitivity: .low, value: value)
			case .sensitivityMiddle:
				MyntParamConfig.shared.setAlarmDelay(sensitivity: .middle, value: value)
			case .sensitivityHigh:
				MyntParamConfig.shared.setAlarmDelay(sensitivity: .higt, value: value)
			case .frequencyOff:
				MyntParamConfig.shared.setLocationFrequency(frequency: .off, value: value)
			case .frequencySlow:
				MyntParamConfig.shared.setLocationFrequency(frequency: .slow, value: value)
			case .frequencyMiddle:
				MyntParamConfig.shared.setLocationFrequency(frequency: .medium, value: value)
			case .frequencyFast:
				MyntParamConfig.shared.setLocationFrequency(frequency: .fast, value: value)
			}
		}
		return cell!
	}
}




