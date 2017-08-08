import UIKit
import Foundation
import MYNTKit
import SCloudKit
import MapKit
import RealmSwift
import SlightechKit
 
extension SCDevice.SCLocation. `Type` {
	
	var typeName: String {
		switch self {
		case .gps:
			return NSLocalizedString("GPS定位", comment: "")
		case .station:
			return NSLocalizedString("基站定位", comment: "")
		case .mobile:
			return NSLocalizedString("手机定位", comment: "")
		default:
			return ""
		}
	}
}

// MRAK: - Location转CLLocationCoordinate2D
extension SCDevice.SCLocation {
	
	var coordinate: CLLocationCoordinate2D {
		return CLLocationCoordinate2DMake(latitude, longitude)
	}
}

struct MyntMapLocation {
	//经纬度
	var coordinate = CLLocationCoordinate2DZero
}

//底部圆圈
public class MyntCircleAnnotation: NSObject, MKAnnotation {
	
	public var coordinate: CLLovationCoordinate2D {
		willSet {
			willChangeValue(forKey: "coordinate")
		}
		didSet {
			didChangeValue(forKey: "coordinate")
		}
	}

	//GCD初始化
	init(coordinate: CLLocationCoordinate2D) {
		self.coordinate = coordinate
	}
}

class BaseMyntMapViewController: BaseViewController {
	
	class PositionItem: NSObject, CoordinateItemProtocol {

		var time: TimeInterval = 0

		var coordinate: CLLocationCoordinate2D = CLLocationCoordinate2DMake(0, 0)
		var locationType: SCDevice.SCLocation. `Type` = .none

		init(location: SCDevice.SCLocation) {
			self.time 			= TimeInterval(location.updateTime)
			self.coordinate 	= CLLocationCoordinate2DMake(location.latitude, location.longitude).offsetLocation
			self.locationType 	= location.type
		}

		init(userCoordinate: CLLocationCoordinate2D) {
			self.item 			= 0
			self.coordinate 	= userCoordinate
		}

		init(time: TimeInterval,
			coordinate: CLLocationCoordinate2D,
			type: SCDevice.SCLocation. `Type` = .none) {
			self.time 			= time
			self.coordinate 	= coordinate.offsetLocation
			self.locationType 	= type
		}
	}

	override var isNeedAddMyntNotification: Bool {
		return true
	}

	//scrollView当前高度
	let scrollViewHeight: CGFloat = 60

	// MARK: - 组件
	var mapView: MKMapView?

	@IBOutlet weak var mapSuperView: UIView!
	@IBOutlet weak var calendarSuperView: UIView!
	@IBOutlet weak var dataSuperView: UIView!
	//日历控件
	@IBOutlet weak var calendarView: CalendarView!
	@IBOutlet weak var calendarView: UILabel!
	@IBOutlet weak var backLocationButton: GradientButton!
	@IBOutlet weak var buttonsView: MyntButtonsView!
	//地图时间轴控件
	@IBOutlet weak var coordinateProgressView: CoordinateProgressView!
	@IBOutlet weak var goView: UIView!
	@IBOutlet weak var goLabel: UILabel!
	//地理位置显示
	@IBOutlet weak var locationLabel: UILabel!
	//地理位置显示时间
	@IBOutlet weak var dateLabel: UILabel!
	//无数据时显示（无数据 Label）
	@IBOutlet weak var noDataLabel: UILabel!

	//MARK: - 约束 scrollView 高度
	@IBOutlet weak var scrollViewHeightConstraint: NSLayoutConstraint!
	//顶部约束
	@IBOutlet weak var mapTopConstraint: NSLayoutConstraint!

	//MARK: - 属性
	override var sn: String! {
		didSet {
			showMapViewContent()
		}
	}
	//小觅头像图标
	var myntAnnotation: MyntAnnotation?
	//小觅图钉底部的圆圈
	fileprivate var myntCircleAnnotation: MyntCircleAnnotation?
	//用户位置(已偏移过)
	public var userCoordinate = CLLocationCoordinate2DZero {
		didSet {
			guard let mynt = sn?.mynt else { return }
			if mynt.bluetoothState == .connected {
				selectedPosition = PositionItem(userCoordinate: userCoordinate)
			}
		}
	}
	//选择位置（已偏移过）
	var selectedPosition: PositionItem? {
		didSet {
			coordinateProgressView?.selectedTime = selectedPosition?.time
			//更新位置
			selectedPosition?.coordinate.reverseGeocodeLocation { [weak self] address in
				self?.locationLabe.text = address
				if let timeType = self?.coordinateProgressView.timeType {
					self?.dateLabel.text = self?.selectedPosition?.time == 0 ?
						NSLocalizedString("DISCONNECT_TIME_NOW", comment: "现在") :
						self?.selectedPosition?.time.timeString(timeType: timeType)
				}
			}
		}
	}
	//列表最终显示的数据源(已偏移过)
	var locations: [PositionItem] = [] {
		didSet {
			coordinateProgressView.selectedTime = selectedPositon?.time
			coordinateProgressView.setData(items: locations.sorted(by: { $0.time > $1.time }).filter { $0.locationType != .station })
		}
	}

	//图钉图片
	var annotationImage: UIImage?

	deinit {
		printDeinitLog()
	}

	override func viewDidLoad() {
		super.viewDidLoad()

		guard let mynt = sn?.mynt else { return }
		title = NSLocalizedString("MAP", comment: "地图")
		setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))
		if mynt.myntType == .myntGPS {
			setRightBarButtonItem(image: UIImage(named: "titlebar_more"))
		}

		//初始化UI
		initUI()

		MYNTKit.shared.addMyntKitDelegate(key: selfKey, delegate: self)
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	//初始化UI
	fileprivate func initUI() {
		scrollViewHeightConstraint.constant = 0

		calendarView.delegate 		= self
		//初始化按钮
		buttonView.sn 		  		= sn
		buttonView.viewController   = self

		backLocationButton.layer.masksToBounds 	= true
		backLocationButton.layer.cornerRadius 	= backLocationButton.bounds.height / 2
		backLocationButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)

		goView.layer.cornerRadius 	= goView.bounds.height / 2
		goView.backgroundColor 		= ColorStyle.kGreenGradientColor.start
		goView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickNavigationButton(_ :))))

		goLabel.text 				= NSLocalizedString("NAVIGATION_GO", comment: "导航")
		noDataLabel.text 			= NSLocalizedString("MYNTSETTING_MAP_NODATA", comment: "没有数据")

		loadAvatar()
	}

	override func viewWillAppear(_ animated: Bool) {
		super.viewWillAppear(animated)
		initMapView()
	}

	override func viewDidAppear(_ animated: Bool) {
		super.viewDidAppear(animated)
		showMapViewContent()
	}

	override func viewDidDisappear(_ animated: Bool) {
		navigationController?.dismiss(animated: true, completion: nil)
		MYNTKit.shared.removeMyntKitDelegate(key: selfKey)
	}

	//MARK: - 导航按钮事件
	func didClickNavigationButton(_ sender: AnyObject) {
		guard let selectedPositon = selectedPositon else { return }

		if !selectedPosition.coordinate.isNull {
			MapNavigationKit.shared.selectMapApp(fromCoordinate: userCoordinate,
												 toCoordinate: selectedPosition.coordiante,
												 view: veiw)
		}
	}

	//回到我的位置
	@IBAction func didClickUserLocationButton(_ sender: AnyObject) {
		if !userCoordinate.isNull {
			mapView?.gotoCoordinate(userCoordinate, range: 3000)
		}
	}

	//MARK: - 更新属性

	//更新选中位置
	func updateSelectCoordinate(coordinate: CLLocationCoordinate2D, range: Double = 5000, time: Int? = nil) {
		if selectedCoordinate == coordinate {
			updateLobel(address: nil, time: time)
			return
		}
		
	}
}























