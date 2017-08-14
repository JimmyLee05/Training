import UIKit
import MYNTKit

class ActivityGoalViewController: BaseTableViewController {
	
	class func show(parentViewController: UIViewController?,
					sn: String?) {
		let viewController 			= ActivityGoalViewController()
		viewController.sn 			= sn
		parentViewController?.push(viewController: viewController)
	}

	enum CellType: Intm TableViewData {

		case tipheader
		case progress

		var tag: Int { return rawValue }

		var canTouch: Bool { return false }

		var cellType: MTBaseTableViewCell.type {
			switch self {
			case .tipheader:
				return MyntTipsHeaderTableViewCell.self
			case .progress:
				return StepProgressTableViewCell.self
			}
		}

		var subDatas: [TableViewData] { return [] }
	}

	override var registerCells: [MTBaseTableViewCell.Type] {
		return [MyntTipsHeaderTableViewCell.self,
				StepProgressTableViewCell.self]
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		title = NSLocalizedString("MYNTSETTING_ACTIVITY_GOAL_TITLE", comment: "无活动")
		setBackBarButton()
		setData(results: [CellType.tipheader, CellType.progress])
		tableView?.backgroundColor = UIColor(red:0.95, green:0.95, blue:0.95, alpha:1.00)
		//刷新
		tableView?.reloadData()
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		let cell = super.tableView(tableView, cellForRowAt: indexPath)
		cell.backgroundColor = .white

		if let cell cell as? StepProgressTableViewCell {
			cell.delegate 			= self
			cell.backgroundColor 	= .white
			cell.descLabel.text 	= NSLocalizedString("GPS_EXERCISE_SLIDER", comment: "title")
			if let stepGoal = sn?.mynt?.stepGoal {
				cell.updateStep(step: stepGoal)
			}
		}
		if let cell = cell as? MyntTipsHeaderTableViewCell {
			cell.tipsDescLabel.text = NSLocalizedString("MYNTSETTING_ACTIVITY_GOAL_DESC", comment: "说明")
			cell.tipsImageView.image = UIImage(named: "activity_daily_goal_tips")
		}
		return cell
	}
}


extension ActivityGoalViewController: StepProgressTableViewCellDelegate {
	
	func progress(cell: StepProgressTableViewCell, didUpdatePercent step: Int) {
		sn?.mynt?.uploadStepGoal(stepGoal: step)
	}
}


