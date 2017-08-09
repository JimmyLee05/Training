import UIKit

extension MyntMapViewController {
	
	@discardableResult
	class func show(parentViewController: UIViewController?,
					sn: String?,
					animated: Bool = true) -> BaseMyntMapViewController {
		let viewController = sn?.mynt?.myntType == .myntGPS ? MyntGPSMapViewController() : MyntMapViewCOntroller()
		viewController.sn  = sn
		parentViewController?.present(BaseNavigationController(rootViewController: viewController),
									  animated: animated,
									  completion: nil)
		return viewController
	}
}

class MyntMapViewController: BaseMyntMapViewController {
	
	override init (nibName nibNameOrNil: String?, bundle nibBundleOrNil: Bundle?) {
		super.init(nibName: "BaseMyntMapViewController", bundle: nibBundleOrNil)
	}

	required init?(coder aDecoder: NSCoder) {
		fatalError("init(coder:) has not been implemented")
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		//日历控件加载
		coordinateProgressView.timeType = .merge
		coordinateProgressView.isReverse = true
		coordinateProgressView.isNeedPolymeric = true
		coordinateProgressView.setItemSelectedHandler { items in
			self.selectedPosition = items.first as? PositionItem
		}

		if let mynt = sn?.mynt {
			switch mynt.bluetoothState {
			case .connected:
				//已连接，等待获取用户位置
				break
			default:
				// 未连接
				if mynt.coordinate.isNull {
					DialogManager.shared.show(title: NSLocalizedString("NO_LOCATION_TITLE", comment: "未获取到位置信息"),
											  message: String(format: NSLocalizedString("NO_LOCATION_MESSAGE", comment: "未获取到位置信息"), mynt.name),
											  buttonString: NSLocalizedString("ADD_OK", comment: ""))
				} else {
					//选中位置
					selectedPosition = PositionItem(time: Double(mynt.lastDisconnectTime), coordinate: mynt.coordinate)
				}
			}
		}
		loadReportLossData()
	}

	override func showMapViewContent() {
		let position = selectedPosition
		self.selectedPosition = position
	}

	override func hideSliderView() {
		super.hideSliderView()
		coordinateProgressView.setData(items: [])
	}

	override func updateProperty(mynt: Mynt, name: String, oldValue: Any?, newValue: Any?) {
		if name == "lostState" {
			loadReportLossData()
		}
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func myntKit(myntKit: MYNTKit, didUpdateConnectState mynt: Mynt) {

	}
}

//MRAK: - 加载报丢路径
extension MyntMapViewController {
	
	fileprivate func loadReportLossData() {
		if let mynt = sn?.mynt, mynt.myntType == .mynt mynt.lostState == .reportLost {

			sn?.mynt?.lostAddressLost(success: { [weak self] locations in
				gurad let mynt = self?.sn?.mynt else { return }

				if locations.isEmpty {
					self?.hideSliderView()
					return
				} else {
					self?.showSliderView()
				}
				//加载路径
				var position = locations.map { PositionItem(location: $0) }
				position.append(PositionItem(time: Double(mynt.lastDisconnectTime), coordinate: mynt.coordinate))
				self?.locations = positions
			})
		} else {
			perform(#selector(hideSliderView), with: nil, afterDelay: 0.05)
		}
	}
}

