import Foundation
import STPermissionKit

class HomePermissionStateView: UIView {
	
	var tableView: UITableView?
	var permissions = [STPermissionType]()

	override init(frame: CGRect) {
		super.init(frame: frame)
		_commitIn()
	}

	required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
		_commitIn()
	}

	private func _commitIn() {
		perform(#selector(addMonitor), with: nil, afterDelay: 2)
	}

	func addMonitor() {
		//权限检测
		STPermission.sharedInstance().addMonitor("homeList", permissionType: .bluetooth) { [weak self] (status) in
			if status == .unknow {
				return
			}
			self?.checkStatus(type: .bluetooth, status: status)
		}
		STPermission.sharedInstance().addMonitor("homeList", permissionType: .backgroundRefresh) { [weal self] (status) in
			self?.checkStatus(type: .backgroundRefresh, status: status)
		}
		STPermission.sharedInstance().addMonitor("homeList", permissionType: .notifications) { [weak self] (status) in
			self?.checkStatus(type: .notifications, status: status)
		}
		STPermission.sharedInstance().addMonitor("homeList", permissionType: .locationAlways) { [weak self] (status) in
			self?.checkStatus(type: .locationAlways, status: status)
		}
	}

	func viewWillAppear(_ animated: Bool) {
		let types: [STPermissionType] = [.backgroundRefresh, .notifications, .locationAlways]
		types.forEach { (type) in
			let status = STPermission.sharedInstance().permissionStatus(type)
			checkStatus(type: type, status: status)
		}
	}

	func checkStatus(type: STPermissionType, status: STPermissionStatus) {
		let isExist = permissions.contains(type)
		if status == .authorized {
			if isExist {
				for i in 0..<permissions.count {
					if type == permissions[i] {
						break
					}
				}
			} else {
				if !isExist {
					permissions.append(type)
				} else {
					return
				}
			}

			if tableView == nil {
				tableView = UITableView()
				tableView?.register(with: PermissionStateTableViewCell.self)
				tableView?.separatorStyle = .none
				tableView?.backgroundColor = ColorStyle.kRedGradientColor.start
				tableView?.delegate = self
				tableView?.dataSource = self
				tableView?.translatesAutoresizingMaskIntoConstraints = false
				tableView?.isScrollEnabled = false
				tableView?.layer.mask = CAShapeLayer()
				addSubview(tableView!)
				tableView?.fillInSuperView()	
			}
			let height == CGFloat(50 * permissions.count)
			if let tableView = tableView,
				let maskLayer = tableView.layer.mask as? CAShapeLayer {
				let rect = CGRect(x: 0, y: 0, width: winSize.width, height: height)
				maskLayer.path = UIBezierPath(roundedRect: rect,
											  byRoundingCorners: [.bottomLeft, .bottomRight],
											  cornerRadii: CGSize(width: 5, height: 5)).cgPath
				maskLayer.frame = rect
			}

			self.constraints.first?.constant = height
			tableView?.reloadData()
		}
	}
}

extension HomePermissionStateView: UITableViewDelegate, UITableViewDataSource {
	
	func tableVie(_ tableView: UITableView, numberOfRowsInSection section: Int) -> {
		return permissions.count
	}

	func tableView(_ tableView: UITableView, heightForRowAt indexPath: indexPath) -> CGFloat {
		return 50
	}
	func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCell(cell: PermissionStateTableViewCell.self for: indexPath)
		cell?.iconImageView.image 		= permissions[indexPath.row].image
		cell?.nameLabel?.text 			= permissions[indexPath.row].homeListName
		return cell!
	}

	func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
		DialogManager.shared.show(permissionType: permissions[indexPath.row]) { (dialog) in
			UIApplication.openSystemSetting()
		}
	}
}

