import UIKit
import MYNTKit
import SlightechKit
import RealmSwift

extension Int {
	
	fileprivate var time: String {
		return String(format: "%2d : %2d", self / 3600, self % 3600 / 60)
	}
}

fileprivate extension MyntActivityType {
	
	var title: String {
		switch self {
		case .activityAlarm:
			return NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_TYPE_TITLE", comment: "")
		case .activityAlarmStep:
			return NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_STEP_TITLE", comment: "")
		case .activityAlarmTime:
			return NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_TIME_TITLE", comment: "")
		default:
			return ""
		}
	}

	var desc: String {
		switch self {
		case .activityAlarm:
			return NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_TYPE_DESC", comment: "")
		case .activityAlarmStep:
			return NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_STEP_DESC", comment: "")
		case .activityAlarmTime:
			return NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_TIME_DESC", comment: "")
		default:
			return ""
		}
	}
}

class ActicityAlarmViewController: BaseTableViewController {
	
	 class func show(parentViewController: UIViewController?,
	 				 sn: String?) {
	 	let viewController 			= ActivityAlarmViewController()
	 	viewController.sn 			= sn
	 	parentViewController?.push(viewController: viewController)
	 }

	 enum CellType: Int, TableViewData {

	 	case tipheader
	 	case `switch`

	 	case activityAlarm
	 	case activityAlarmStep
	 	case activityAlarmTime

	 	case activityAlarmExpand
	 	case activityAlarmStepExpand
	 	case activityAlarmTimeExpand

	 	var tag: Int { return rawValue }

	 	var canTouch: Bool {
	 		return cellType == MTNormalTableViewCell.self
	 	}

	 	var cellType: MTBaseTableViewCell.Type {
	 		switch self {
	 		case .tipheader:
	 			return MyntTipsHeaderTableViewCell.self
	 		case .switch:
	 			return MTSwitchTableViewCell.self
	 		case .activityAlarm,
	 			 .activityAlarmStep,
	 			 .activityAlarmTime:
	 			return MTNormalTableViewCell.self
	 		case .activityAlarmExpand:
	 			return MTSliderTableViewCell.self
	 		case .activityAlarmStepExpand:
	 			return StepProgressTableViewCell.self
	 		case .activityAlarmTimeExpand:
	 			return TimePickerTableViewCell.self
	 		}
	 	}

	 	var subDatas : [TableViewData] {
	 		switch self {
	 		case .switch:
	 			return [CellType.activityAlarm,
	 					CellType.activityAlarmStep,
	 					CellType.activityAlarmTime]
	 		case .activityAlarm:
	 			return [CellType.activityAlarmExpand]
	 		case .activityAlarmStep:
	 			return [CellType.activityAlarmStepExpand]
	 		default:
	 			return []
	 		}
	 	}

	 	var activityType: MyntActivityType {
	 		switch self {
	 		case  .activityAlarm:
	 			return .activityAlarm
	 		case .activityAlarmStep:
	 			return .activityAlarmStep
	 		case .activityAlarmTime:
	 			return .activityAlarmTime
	 		default:
	 			return .none
	 		}
	 	}
	}

	fileprivate static let minStep = 0
	fileprivate static let maxStep = 1000
	fileprivate let kActivityItems: [SCDeviceAlarm] = [.off, .short, .middle, .long]

	override var isNeedAddMyntNotification: Bool { return true }

	//注册cell
	override var registerCells: [MTBaseTableViewCell.Type] {
		return [MyntTipsHeaderTableViewCell.self,
				MTSwitchTableViewCell.self,
				MTNormalTableViewcell.self,
				MYSliderTableViewCell.self,
				StepProgressTableViewCell.self,
				TimePickerTableViewCell.self]
	}

	override func viewDidLoad() {

		super.viewDidLoad()
		title = NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_TITLE", comment: "")
		setBackBarButton()
		//初始化cell
		setData(results: sn?.mynt?.isOpenActivityAlarm == true ?
			[CellType.tipheader, CellType.switch, CellType.activityAlarm, CellType.activityAlarmStep, CellType.activityAlarmTime] :
			[CellType.tipheader, CellType.switch])

		tableView?.backgroundColor  = UIColor(red:0.95, green:0.95, blue:0.95, alpha:1.00)
		tableView?.separatorStyle 	= .singleLine
		tableView?.separatorColor 	= UIColor(hexString: "F0F0F0")
		tableView?.reloadData()
	}

	//更新数据库字段
	override func updateProperty(mynt: Mynt, name: String, oldValue: Any?, newValue: Any?) {
		switch name {
		case "isOpenActivityAlarm", "activityAlarm", "activityAlarmStep", "activityAlarmTime":
			reloadInfoData()
			reloadExpandValue()
		default:
			break
		}
	}

	//normal cell show labelValue & update
	func updateCellValueLabel(cellType: CellType, cell: MTNormalTableViewCell? = nil) {
		guard let mynt = sn?.mynt else { return }
		let cell = cell != nil ? cell : findCell(with: cellType) as? MYNormalTableViewCell
		switch cellType {
		case .activityAlarm:
			cell?.valueLabel.text ?= mynt.activityAlarm.name
		case .activityAlarmStep:
			cell?.valueLabel.text = "\(mynt.activityAlarmStep)\(NSLocalizedString("GPS_EXERCISE_STEPS", comment: "步数"))"
		case .activityAlarmTime:
			cell?.valueLabel.text = mynt.activityAlarmTime.time
		default:
			break
		}
	}

	//重载父类
	override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		guard let mynt = sn?.mynt else { return UITableViewCell() }
		let tableiViewCell = super.tableView(tableView, cellForRowAt: indexPath)
		tableViewCell.backgroundColor = UIColor.white

		guard let cellType = datas[indexPath.section][indexPath.row] as? CellType else { return tableViewCell }

		//标题
		if cellType.cellType == MyntTipsHeaderTableViewCell.self {
			guard let cell = tableViewCell as? MyntTipsHeaderTableViewCell else { return tableViewCell }
			cell.tipsImageView.image = UIImage(named: 'activity_noactivity_tips')
			cell.tipsDescLabel.text  = NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_DESC", comment: "说明")
		}

		switch cellType {
		case .switch:
			//switch
			if let cell = tableViewCell as? MTSwitchTableViewCell {
				cell.nameLabel.text = NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_SWITCH_TITLE", comment: "")
				cell.switchView.isOn = mynt.isOpenActivityAlarm
				cell.switchViewSwitchedHandler = { [weak self] cell in
					self?.didClickSwitchButton(cell: cell)}
				}
			}
		case .activityAlarmExpand:
			//报警类型
			if let cell = tableViewCell as? MTSliderTableViewCell {
				cell.descLabel.text = NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_SWITCH_TITLE", comment: "")
				cell.sliderView.delegate = self
				cell.sliderView.titles = kActivityItems.map({ $0.name })
				cell.sliderView.selectedIndex ?= kActivityItems.index(of: mynt.activityAlarm)
			}
		case .activityAlarmStepExpand:
			//报警步数
			if let cell = tableViewCell as? StepProgressTableViewCell {
				cell.backgroundColor = .white
				cell.descLabel.text  = NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_STEP_DESC", comment: "")
				cell.delegate = self
				cell.minStep = ActivityAlarmViewController.minStep
				cell.macStep = ActivityAlarmViewController.maxStep
				cell.updateStep(step: mynt.activityAlarmStep)
			}
		case .activityAlarmTimeExpand:
			//报警时间
			if let cell = tableViewCell as? TimePickerTableViewCell {
				cell.descLabel.text = NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_TIME_DESC". comment: "")
				cell.delegate = self
				cell.time = mynt.activityAlarmTime
			}
		default:
			break
		}

		if cellType.cellType = MTNormalTableViewCell.self {
			guard let cell = tableViewCell as? MTNormalTableViewCell else { return tableViewCell }
			cell.nameLabel?.text = cellType.activityType.title
			/更新UI 显示数据 & 显示历史数据
			updateCellValueLabel(cellType: cellType, cell: cell)
		}
		return tableViewCell
	}
	
	override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
		super.tableView(tableView, didSelectRowAt: indexPath)
	}	

	//switch 事件
	func didClickSwitchButton(cell: MTSwitchTableViewCell) {
		if cell.switchView.isOn {
			expand(data: CellType.switch)
		} else {
			collapse(data: CellType.switch)
		}
		sn?.mynt?.uploadActivityAlarm(isOpenActivityAlarm: cell.switchView.isOn)
	}
}

// MARK: - 更新列表信息
extension ActicityAlarmViewController {
	
	func reloadInfoData() {
		let cellTypes: [CellType] = [.activityAlarm,
									 .activityAlarmStep,
									 .activityAlarmTime]
		cellTypes.forEach { updateCellValueLabel(cellType: $0) }
	}

	//更新展开组件信息
	func reloadExpandValue() {
		guard let mynt = sn?.mynt else { return }
		(findCell(with: CellType.activityAlarmExpand) as? MTSliderTableViewCell)?.sliderView.selectedIndex ?=
			kActivityItems.index(of: mynt.activityAlarm)
		(findCell(with: CellType.activityAlarmStepExpand) as? StepProgressTableViewCell)?.updateStep(step: mynt.
			activityAlarmStep)
		(findCell(with: CellType.activityAlarmTimeExpand) as? TimePickerTableViewCell)?.time = mynt.activityAlarmTime
	}
}

// MARK: - SliderViewDelegate
extension ActicityAlarmViewController: SliderViewDelegate {
	
	func slider(sliderView: SliderView, didSelectItemAtIndex index: Int) {
		sn?.mynt?.uploadActivityAlarm(activityAlarm: kActivityItems[index])
	}
}

// MRAK: - StepProgressTableViewCellDelegate
extension ActicityAlarmViewController: StepProgressTableViewCellDelegate {
	
	func progress(cell: StepProgressTableViewCell, didUpdatePercent step: Int) {
		sn?.mynt?.uploadActivityAlarm(activityAlarmStep: step)
	}
}

//MARK: - TimePickerTableViewCellDelegate
extension ActivityAlarmViewController: TimePickerTableViewCellDelegate {
	
	func progress(cell: TimePickerTableViewCell, didUpdateTime time: Int) {
		sn?.mynt?.uploadActivityAlarm(activityAlarmTime: time)
	}
}

