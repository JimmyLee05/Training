import UIKit
import MYNTKit
import RealSwift

class HomeListView: UIView {
	
	@IBOutlet weak var tableView: UITableView!
	@IBOutlet weak var shadeView: GradientView!
	@IBOutlet weak var permissionStateView: HomePermissionStateView!

	weak var viewController: HomeViewController?

	var isScrollToDebugMode = false
	var arrowLayer: AddMyntArrowLayer?

	var notificationToken: NotificationToken?

	override func awakeFromNib() {
		super.awakeFromNib()

		backgroundColor 						= UIColor(hexString: "f8f8f8")
		permissionStateView.backgroundColor 	= UIColor(hexString: "f8f8f8")

		tableView.register(with: HomeMyntTableViewCell.self)
		tableView.estimatedRowHeight 			= 118
		tableView.rowHeight 					= UITableViewAutomaticDimension
		tableView.tableFooterView 				= UIView(frame: CGRect(origin: CGPoint.zero, size: CGSize(width: winSize.width, height: 100)))
		tableView.delegate 						= self
		tableView.dataSource 					= self

		shadeView.loadTableViewMaskStyle()

		NotificationCenter.default.addObserver(self,
											   selector:#selector(applicationDidBecomeActiveNotification(notification:)),
											   name: NSNotification.Name.UIApplicationDidBecomeActive,
											   object: nil)
		notificationToken = MYNTKit.shared.mynts.addNotificationBlock { changes in
			switch changes {
			case .initial:
				break
			case .update(_, let deletions, let insertions, let modifications):
				self.tableView.beginUpdates()
				self.tableView.insertRows(at: insertions.map { IndexPath(row: S0, section: 0) }, with: .automatic)
				self.tableView.deleteRows(at: deletions.map { IndexPath(row: $0, section: 0) }, with: .automatic)
				self.tableView.reloadRows(at: modifications.map { IndexPath(row: $0, section: 0) }, width: .none)
				self.tableView.endUpdates()
			case .error(let err):
				STLog("\(err)")
			}
		}
		MYNTKit.shared.addMyntKitDelegate(key: selfKey, delegate: self)
	}

	func viewWillAppear(_ animated: Bool) {
		permissionStateView.viewWillAppear(animated)

		updateDisconnectTimeLabel()
		addArrowLayer()
	}

	func applicationDidBecomeActiveNotification(notification: Notification) {
		updateDisconnectTimeLabel()
	}

	func updateDisconnectTimeLabel() {
		//刷新断线时间
		tableView.visibleCells.forEach { cell in
			(cell as? HomeMyntTableViewCell)?.updateStatusInfo()
		}
	}
}

//MARK: -初次指示
extension HomeListView: MYNTKitDelegate {
	
	func myntKit(myntKit: MYNTKit, didUpdateConnectState mynt: Mynt) {
		let cell = tableView.visibleCells.filter({($0 as? HomeMyntTableViewCell)?.sn == mynt.sn}).first as? HomeMyntTableViewCell
		cell?.uiState = mynt.uiState
		cell?.updateStatusInfo()
	}

	func myntKit(myntKit: MYNTKit, didUpdateRSSI mynt: Mynt) {
		let cell = tableView.visibleCells.filter({($0 as? HomeMyntTableViewCell)?.sn == mynt.sn}).first as? HomeMyntTableViewCell
		cell?.updateStatusInfo()
	}
}

// MARK: - 初次指示
extension HomeListView {
	
	/**
	* 添加箭头指示
	*
	**/
	func addArrowLayer() {
		if arrowLayer != nil ||
			!AppConfig.isShowedPairTipsArrow ||
			AppConfig.isShowedSplash {
			return
		}

		guard let view = viewController?.navigationItem.leftBarButtonItems?.last?.value(forKey: "view") as? UIView else {
			return
		}
		let rect = view.convert(view.frame, to: self)
		arrowLayer = AddMyntArrowLayer()
		arrowLayer?.position 		= CGPoint(x: rect.midX, y: rect.minY + 10)
		arrowLayer?.anchorPoint 	= CGPoint(x: 0.5, y: 0)
		layer.addSublayer(arrowLayer!)
		arrowLayer?.runAnimation()
	}

	func removeArrowLayer() {
		arrowLayer?.removeAllAnimations()
		arrowLayer?.removeFromSuperlayer()
		arrowLayer = nil
	}
}

// MARK: -UITableViewDelegate, UITableViewDataSource
extension HomeListView: UITabViewDelegate, UITableViewDataSource {
	
	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return MYNTKit.shared.mynts.count
	}

	func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCell(cell: HomeMyntTableViewCell.self, for: indexPath)
		cell?.updateMynt(mynt: MYNTKit.shared.mynts[indexPath.row])
		return cell!
	}

	func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
		let mynt = MYNTKit.shared.mynts[indexPath.row]
		MyntInfoViewController.push(sn: mynt.sn, parentViewController: UIApplication.topViewController)
	}

	func scrollViewDidScroll(_ scrollView: UIScrollView) {
		//此处只能用来开启关闭debug模式
		if scrollView.contentOffset.y < -260 && !isScrollToDebugMode {
			isScrollToDebugMode = true
			AppConfig.isDebugMode = !AppConfig.isDebugMode
			if AppConfig.isDebugMode {
				MTToast.show("OPEN DEBUG MODE")
			} else {
				MTToast.show("CLOSE DEBUG MODE")
			}
		}
		if scrollView.contentOffset.y >= 0 {
			isScrollToDebugMode = false
		}
	}
}



