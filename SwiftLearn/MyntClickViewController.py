import UIKit
import MYNTKit
import SlightechKit
import RealmSwitch

class MyntClickViewController: BaseViewController {
	
	@discardableResult
	class func show(parentViewController: UIViewController?,
					sn: String?,
					clickEvent: MYNTClickEvent) -> MyntClickViewController {
		let viewController 						= MyntClickViewController()
		viewController.sn 						= sn
		viewController.selectedClickEvent 		= clickEvent
		parentViewController?.navigationController?.pushViewController(viewController, animated: true)
		return viewController
	}

	enum CellType {

		case clickTypeCell
		case clickValyeCell

		var height: CGFloat {
			switch self {
			case .clickTypeCell:
				return 200
			default:
				return 55
			}
		}
	}

	override var isNeedAddMyntNotification: Bool { return true }
	override var isShowBackgroundLayer: Bool { return true }

	@IBOutlet weak var tableView: UITableView!

	// collectionView数据源
	fileprivate let controlCategories: [MyntControlCategory] = [.camera, .music, .ppt, .phone]
	// tableview数据源
	fileprivate var clickValues: [SCClickValue] = []
	// cell类型
	fileprivate var cellTypes = [CellType]()
	//选中的相机类型(相机， 音乐， ppt， 手机)
	fileprivate var selectedControlCategory: MyntControlCategory = .camera {
		didSet {
			_updateClickValues()
		}
	}
	//选中的手势(单击，双击，三击，长按， 单击 + 长按)
	var selectedClickEvent: MYNTClickEvent = .click {
		didSet {
			_updateClickValues()
		}
	}

	deinit {
		printdeinitLog()
		MYNTKit.shared.removeMyntKitDelegate(key: selfKey)
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		tableView.register(with: MyntConfigCollectionTableViewCell.self)
		tableView.register(with: MyntControlClickValueTableViewCell.self)
		title = selectedClickEvent.name

		setBackBarButton()

		cellTypes = [.clickTypeCell, .clickValueCell]
		tableView.tableHeaderView 	 = UIView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: 0))
		tableView.tableFooterView 	 = UIView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: 100))
		tableView.delegate 			 = self
		tableview.dataSource 		 = self
		tableview.addBottomWhiteView(offSetY: navigationBarHeight + 135)

		controlCategories.forEach { myntControlCategory in
			guard let selectedClickValue = self.selectedClickValue() else { return }
			if myntControlCategory.base().contains(selectedClickValue) {
				selectedControlCategory = myntControlCategory
			}
		}		
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	private func _updateClickValues() {
		if selectedClickEvent == .click ||
			selectedClickEvent == .doubleClick ||
			selectedClickEvent == .tripleClick {
			clickValues = selectedControlCategory.click
			tableView?.reloadData()
		}  else {
			guard let mynt = sn?.mynt else { return }
			clickValues = selectedControlCategory.longClick(myntMynt: mynt.myntType)
			tableView?.reloadData()
		} 
	}

	func _updateClickValue(clickValue: SClickValue) {
		guard let mynt = sn?.mynt else { return }
		let event = selectedClickEvent
		let controlValue = mynt.controlValue
		mynt.update {
			switch event {
			case .click:
				controlValue.click = clickValue
			case .doubleClick:
				controlValue.doubleclick = clickValue
			case .tripleClick:
				controlValue.tripleClick = clickValue
			case .hold:
				controlValue.hold = clickValue
			case .clickHold:
				controlValue.clickHold = clickValue
			default:
				break
			}
		}

		mynt.setControlValue(controlValue: controlValue)
		tableView.reloadData()
	}
}

extension MyntClickViewController: UITableViewDelegate, UITableViewDataSource {
	
	func nubmerOfSection(in tableView: UITableView) -> Int {
		return cellTypes.count
	}

	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		if section == 0 {
			retur 1
		} else {
			if let mynt = sn?.mynt {
				return selectedControlCategory.base(myntType: mynt.myntType).count
			}
			return 0
		}
	}

	func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
		return cellTypes[indexPath.section].height
	}

	//数据源
	func tableView(_ tableView: UITableFView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		let cellType = cellType[indexPath.section]
		switch cellType {
		case .clickTypeCell:
			let cell = tableView.dequeueReusableCell(cell: MyntConfigCollectionTableViewCell.self, for: indexPath)
			cell?.delegate = self
			cell?.hintLabel.text = NSLocalizedString("CONTROL_CONTROLTYPE_TIPS", comment: "")
			cell?.hintLabel.textColor = UIColor.white
			return cell!
		case .clickValueCell:
			let cell = tableView.dequeueReusableCell(cell: MyntControlClickValueTableViewCell.self, for: indexPath)
			if let mynt = sn?.mynt {
				let clickValue = selectedControlCategory.base(myntType: mynt.myntType)(indexPath.row)
				cell?.clickValue = clickValue
				cell?.iconImageView.image = clickValue.smallAvatar?.withRenderingMode(.alwaysTemplate)
				cell?.clickValueLabel.text = clickValue.name
				cell?.linkButtonClickedHandler = { [weak self] value, isSelected in
					self?.updateClickValue(clickValue: isSelected ? .none : value)
				}
				let isSelected = selectedClickValue() == clickValue
				cell?.state = isSelected ? .selected : clickValues.contains(clickValue) ? .normal : .disable
			}
			return cell!
		}
	}

	fileprivate func selectedClickValue() -> SCClickValue? {
		switch selectedClickEnent {
		case .click:
			return sn?.mynt?.controlValue.click
		case .doubleClick:
			return sn?.mynt?.controlValue.doubleclick
		case .tripleClick:
			return sn?.mynt?.controlValue.tripleClick
		case .hold:
			return sn?.mynt?.controlValue.clickHold
		default:
			return .none
		}
	}
}

// MARK: MyntConfigCollectionTableViewCellDelegate
extension MyntClickViewController: MyntConfigCollectionTableViewCellDelegate {
	
	func numberOfCell(cell: MyntConfigCollectionTableViewCell) -> Int {
		return controlCategories.count
	}

	//数据源
	func collection(cell: MyntConfigCollectionViewTableCell, didUpdateCellAt index: Int, collectionCell:
		MyntConfigCollectionCell?) {
		collectionCell?.iconWidthConstraint.constant 	= 40
		collectionCell?.iconImageView.image 			= controlCategories[index].image?.withRenderingMode(.
			alwaysTemplate)
		collectionCell?.valueLabel.text 				= controlCategories[index].name
		collectionCell?.titleLabel.text 				= ""
		collectionCell?.state 							= controlCategories[index] ==
			selectedControlCategory ? .selected : ,normal
		collectionCell?.valueLabel.textColor 			= UIColor.white
	}

	//点击事件，更新每个 clickType的 clickValue的值
	func collection(cell: MyntConfigCollectionTableViewCell, didSelectedAt index: Int?) {
		//点击类型
		guard let index = index else { return }
		selectedControlCategory = controlCategories[index]
	}

}


