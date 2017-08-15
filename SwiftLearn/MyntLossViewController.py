import UIKit
import SlightechKit

extension MyntLossType {
	
	fileprivate var tipsDesc: String {
		switch self {
		case .phontAlarm:
			return NSLocalizedString("MYNTSETTING_LOSS_PHONEALARM_DESC", comment: "")
		case .myntAlarm:
			return NSLocalizedString("MYNTSETTING_LOSS_MYNTALARM_DESC", comment: "")
		case .sensitivity:
			return NSLocalizedString("MYNTSETTING_LOSS_SENSITIVITY_DESC", comment: "")
		case .locationFrequeucy:
			return NSLocalizedString("MYNTSETTING_LOSS_FREQUEUY_DESC", comment: "")
		default:
			return ""
		}
	}

	fileprivate var tipsImage: UIImage? {
		switch self {
		case .phoneAlarm:
			return NSLocalizedString("MYNTSETTING_LOSS_PHONEALARM_DESC", comment: "")
		case .myntAlarm:
			return NSLocalizedString("MYNTSETTING_LOSS_MYNTALARM_DESC", comment: "")
		case .sensitivity:
			return NSLocalizedString("MYNTSETTING_LOSS_SENSITIVITY_DESC", comment: "")
		case .locationFrequeucy:
			return NSLocalizedString("MYNTSETTING_LOSS_FREQUENCY_DESC", comment: "")
		default:
			return ""
		}
	}

	fileprivate var items: [EnumPropertyProtocol] {
		switch self {
		case .phoneAlarm, .mymtAlarm:
			let kAlarmItems: [SCDeviceAlarm] = [.off, .short, .middle, .long]
			return kAlarmItems
		case .sensitivity:
			let kSensitivityItems: [SCSensitivity] = [.high, .middle, .low]
			return kSensitivityItems
		case .locationFrequeucy:
			let kLocationFrequeucyItems: [SCLocationFrequeucy] = [.slow, .medium, .fase]
			return kLocationFrequeucyItems
		default:
			return []
		}
	}

	fileprivate func dbContent(mynt: Mynt) -> EnumPropertyProtocol {
		switch self {
		case .phoneAlarm:
			return mynt.usageValue.phoneAlarm
		case .myntAlarm:
			return mynt.usageValue.myntAlarm
		case .sensitivity:
			return mynt.usageValue.sensitivity
		case .locationFrequeucy:
			return mynt.usageValue.locationFrequeucy
		default:
			return mynt.usageValue.locationFrequency
		}
	}
}

class MyntLossViewController: BaseTableViewController {
	
	class func show(parentViewController: UIViewController?,
					sn: String?,
					lossType: MyntLossType) {
		let viewController 				= MyntLossViewController()
		viewController.myntLossType 	= lossType
		viewController.sn 				= sn
		parentViewController?.push(viewController: viewController)
	}

	enum CellType: Int, TableViewData {
		case tipheader
		case slider

		var tag: Int { return rawValue }

		var canTouch: Bool { return false }

		var cellType: MyntBaseTableViewCell.Type {
			switch self {
			case .tipheader:
				return MyntTipsHeaderTableViewCell.self
			case .slider:
				return MYSliderTableViewCell.self
			}
		}

		var subDatas: [TableViewData] { return [] } 
	}

	var myntLossType: MyntLossType = .phoneAlarm

	override var registerCells: [MTBaseTableViewCell.Type] {
		return [MyntTipsHeaderTableViewCell.self,
				MTSliderTableViewCell.self]
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) ->
		UITableViewCell {
		guard let mynt = sn?.mynt else { return UITableViewCell() }
		let cell = super.tableView(tableView, cellForRowAt indexPath)
		cell.backgroundColor = .white
		if let cell = cell as? MyntTipsHeaderTableViewCell {
			cell.tipsDescLabel.text 		= myntLossType.tipsDesc
			cell.tipsImageView?.image 		= myntLossType.tupsImage
		}

		if let cell = cell as? MTSliderTableViewCell {
			let items = myntLossType.items
			cell.sliderView.delegate = self
			cell.sliderView.titles 	 = items.map { $0.name }
			cell.sliderView.selectedIndex ?= cell.sliderView.titles.index(of: myntLossType.
				dbContent(mynt: mynt).name)
		}
		return cell
	}
}

extension MyntLossViewController: SliderViewDelegate {
	
	func slider(sliderView: SliderView, didSelectItemAtIndex index: Int) {
		guard let mynt = sn?.mynt else { return }
		let usageValue = mynt.usageValue
		mynt.update {
			switch myntLossType {
			case .myntAlarm;
				usageValue.myntAlarm ?= myntLossType.items[index] as? SCDeviceAlarm
			case .phoneAlarm:
				usageValue.phoneAlarm ?= myntLossType.items[index] as? SCDeviceAlarm
			case .sensitivity:
				usageValue.sensitivity ?= myntLossType.items[index] as? SCSensitivity
			case .locationFrequeucy:
				usageValue.locationFrequency ?= myntLossType.items[index] as? SCLocationFrequeucy
			default:
				break
			}
		}
		mynt.setUsageValue(usageValue: usageValue)
	}
}
