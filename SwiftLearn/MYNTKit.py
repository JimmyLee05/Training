import AVFoundationimport FMDBimport Foundationimport INTULocationManagerimport MYNTKit.I18nManagerimport MYNTKit.MTBluetoothimport MYNTKit.MTKeyUtilsimport MYNTKit.MTSystemimport MYNTKit.MTNTKitimport MYNTKit.NSImage_Grayimport MYNTKitimport MYNTKit.Swiftimport MapKitimport MediaPlayerimport MyntCoreBluetoothimport MyntCoreBluetooth.STPrivateFunctionimport Realmimport RealmSwiftimport SCloundKitimport SlightechKitimport SwiftOnoneSupportimport SystemConfiguration.CaptiveNetworkimport SystemConfigurationimport UIKit//! Project version number for MYNTKitpublic var MYNTKitVersionNumber: Doubleextension SCControlMode : EnumPropertyProtocol {		public var name: String { get }	public var image: UIImage? { get }}extension SCControlMode {		public var smallAvatar: UIImage? { get }}extension SCClickValue {		public var name: String { get }	public var smallAvatar: UIImage? { get }}extension UIView {		/**	震动	*/	public func shake(dValue: CGFloat = default, repeatCount: Float = default)}extension UIView {		/**	波纹动画	- parameter color: 波纹颜色	*/	public func rippleAnimate(color: UIColor, scale: CGFloat)}extension SCLocationFrequency {		public static var all: [SCloundKit.SCLocationFrequency]	public init(value: Int?)	public var time: Int { get }}extension SCLocationFrequency : EnumPropertyProtocol {		public var name: String { get }	public var image: UIImage? { get }}extension SCSensitivity {		public static var all: [SCloundKit.SCSensitivity]	public init(value: Int?)	//延迟时间(秒)	public var alarmDelay: Int { get }}extension SCSensitivity : EnumPropertyProtocol {		//名字	public var name: String { get }	public var image: UIImage? { get }}extension CALayer {		public func shake(dValue: CGFloat = default, duration: CFTimeInterval = default, repeatCount: Float = default)}extension UIImage {		public class func create(with radius: CGFloat, padding: CGFloat = default, icon: UIImage?, color: MYNTKit.GradientColor? = default) ->		UIImage?}extension SCDeviceUsage {		public init(value: Int?)	public var myntName: String { get }	public func myntAvatar(mynt: MYNTKit.Mynt) -> UIImage?	public var usageColor: MYNTKit.GradientColor { get }}extension SCDeviceUsage {		public static var all: [SCloundKit.SCDeviceUsage] { get }	public func defaultValue(sn: String) -> MYNTKit.Mynt.Usage }extension SCDeviceUsage: EnumPropertyProtocol {		public var name: String { get }	public var image: UIImage? { get }}/**硬件类型- CC25: CC2541- CC26: CC2640- CC26SE: CC2640 精简- CC26GPS: CC2640 + GPS*/extension MYNTHardwareType {		public var name: String { get }	public var myntType: SCloundKit.SCDeviceType { get }}extension SCDeviceAlarm {		public static var all: [SCloundKit.SCDeviceAlarm]	public init(value: Int?)	//报警次数(次数)	public var alarmCount: Int { get }	//铃声文件名	public var soundName: String { get }}extension SCDeviceAlarm : EnumPropertyProtocol {		//名字	public var name: String { get }	public var image: UIImage? { get }}extension SCloundKit.SCPay.SCOrder {		/**	 *	 *	 */	 public func orderDetail(success: @escaping {SCloudKit.SCPay.SCOrder} -> Swift.Void, failure: MyntFailureHandler)}extension SCDeviceType {		public var name: String { get }	public var typeName: String { get }	public var hardwareTypes: [MYNTHardwareType] { get }}extension SCControlMode {		public static var all: [SCloudKit.SCControlMode]	public func defaultValue(sn: String) -> MYNTKit.Mynt.Control}public class AlarmManager : NSObject, AVAudioPlayerDelegate {		public static let shared: MYNTKit.AlarmManager	/**	执行报警	- parameter soundName: 报警音乐名	*/	public func execAlarm(_ soundName: String?)	/**	取消报警	*/	public func cancelAlarm()	/**	查找手机	- parameter loops: 是否重复播放	*/	public func execFindPhone(_ loops: Bool = default)	/**	停止查找小觅	*/	public func cancelFindPhone()	public func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool)}//主题色public class ColorStyle {		public static let kTunaColor: UIColor	public static let kWriteColor: UIColor	public static let kTunaGradientColor: MYNTKit.GradientColor	public static let kBlueGradientColor: MYNTKit.GradientColor	public static let kRedGradientColor: MYNTKit.GradientColor	public static let kGreenGradientColor: MYNTKit.GradientColor	public static let kOfflineGradientColor: MYNTKit.GradientColor	public static let kGoldTips: MYNTKit.GradientColor	public static let kOrange: MYNTKit.GradientColor	public static let kPortlandOrange: MYNTKit.GradientColor	public static let kCarminePink: MYNTKit.GradientColor	public static let kOliveHaze: MYNTKit.GradientColor	public static let kMantis: MYNTKit.GradientColor	public static let kShamrock: MYNTKit.GradientColor	public static let kSpiroDiscoBall: MYNTKit.GradientColor	public static let kDarkElectricBlue: MYNTKit.GradientColor	public static let kFrenchRose: MYNTKit.GradientColor	public static let kSoftPurple: MYNTKit.GradientColor	public static let kMediumSlateBlue: MYNTKit.GradientColor}public protocol EnumPropertyProtocol {		public var name: String { get }	public var image: UIImage? { get }}/**固件类型- BLE: BLE模式- HID: HID模式*/public enum Firmware {		case ble	case hid	public var name : String { get }}/** * 渐变色 */public struct GradientColor {		public var start: UIColor	public var end: UIColor	public init(start: UIColor, end: UIColor)	public init(color: String)	public var hexString: String { get }}public class JPushManager : NSObject {		public static let shared: MYNTKit.JPushManager	weak public var delegate: JPushManagerDelegate?	public func didReceiveNotification(type: JPushType, info: [AnyHashable : Any])}public protocol JPushManagerDelegate : NSObjectProtocol {		public func push(manager: MYNTKit.JPushManager, didRegisterAlias alias: String?)	public func push(manager: MYNTKit.JPushManager, didRegisterTags tags: [String])	public func push(manager: MYNTKit.JPushManager, didRemoveLocationNotification key: String?)}public class MKImageCache : NSObject {		public static let shared: MYNTKit.MKImageCache	public func downUserAvatar(url: String, handler: @escaping (UIImage?) -> Swift.Void)	public func down(url: String, handler: @escaping (UIImage?) -> Swift.Void)	pubic func load(key: String, handler: @escaping (UIImage?) -> Swift.Void)	public func save(key: String, image: UIImage?)}public func MTLocalizedString(_ key: String, comment: String) -> String/**设备丢失状态- Normal: 正常状态- ReportLost: 报丢状态*/@objc public enum MTMyntLostState : Int {		case normal	case reportLost}public class MTPushMessage : NSObject {		public class func sendMessage(image: UIImage? = default, title: String, subtitle: String)}public class MYNTKit : NSObject {		public static let shared MYNTKit.MYNTKit	public var state: CBCentralManagerState { get }	public var mynts: [MYNTKit.Mynt] { get }	public var user: MYNTKit.User? { get }	public var safeZones: [MYNTKit.SafeZone] { get }	public var isCloseAlarmInSafeZone: Bool	public func initMYNTKit(complete: @escaping () -> Swift.Void)	public func registerJPush()}extension MYNTKit : INTULocationManagerDelegate {		public func locationManager(_ manager: INTULocationManager, didPrintLog log: String)}extension MYNTKit {		public func addMyntKitDelegate(key: String, delegate: MyntKitDelegate)	public func removeMyntKitDelegate(key: String)}extension MYNTKit {		/**		搜索小觅（进行蓝牙搜索）		*/	public func startScan()	/**		搜索小觅 (仅用于搜索新设备)		*/	public func startScanNewMynt(handler: @escaping MYNTKit.ScanHandler)	/**		停止搜索小觅（仅用于搜索新设备）		*/	public func stopScanNewMynt()}extension MYNTKit : SCloudDelegate {		public func cloud(cloud: SCloudKit.SCloud, didRequest url: String, time: TimeInterval)	public func cloud(cloud: SCloudKit.SCloud, didPrintLog log: String)}@objc public protocol MYNTKitDelegate : MyntDelegate, UserDelegate, SafeZoneDelegate {		@objc optional public func myntKit(myntKit: MYNTKit.MYNTKit, didUpdateCentralState state: CBCentralManagerState)	@objc optional public func myntKit(myntKit: MYNTkit.MYNTKit, didAddMynt mynt: MYNTKit.Mynt)	@objc optional public func myntKit(myntkit: MYNTKit.MYNTKit, didRemoveMynt mynt: MYNTKit.Mynt)	@objc optional public func myntKit(myntKit: MYNTKit.MYNTKit, didFoundNewSafeZone safeZone: MYNTKit.SafeZone)	@objc optional public func myntKit(myntKit: MYNTKit.MYNTkit, didReceverAd url: String)}public enum MYNTKitError : Error {		case notGPS}@objc public enum MYNTUIState : Int {		case none	case online	case offline	case report	case connecting}public class MapNavigationKit : NSObject {		public enum MapType {		case apple		case google		case baidu		case amap		case tencent	}	public static let shared: MYNTKit.MapNavigationKit	public func selectMapApp(fromCoordinate: CLLocationCoordinate2D, toCoordinate: CLLocationCoordinate2D, view: UIView)}extension MapNavigationKit : UIActionSheetDelegate {		public func actionSheet(_ actionSheet: UIActionSheet, clickedButtonAt buttonIndex: Int)}public class Mynt : SlightechKit.SKSQLiteModel {		public class Location : NSObject {		public var coordinate: CLLocationCoordinate2D		public var locationTime: TimeInterval		public var locationType: SCloudKit.SCDevice.SCLocation.Type	}	//最后一次断线时间	dynamic public var lastDisconnectTime: Int	//连接类型	dynamic public var connectType: MYNTKit.MyntConnectType	dynamic public var lostState: MYNTKit.MTMyntLostState	dynamic public var name: String	dynamic public var sn: String	dynamic public var iccid: String	dynamic public var firmware: String	dynamic public var hardware: String	dynamic public var software: String	dynamic public var latitude: CLLocationDegress	dynamic public var longitude: CLLocationDegress	dynamic public var radius: Int	dynamic public var locationTime: Int	//分享策略	dynamic public var shareUsersJson: String	//场景	dynamic public var usage: SCloudKit.SCDeviceUsage	//场景颜色	dynamic public var usageColor: String	//场景颜色	dynamic public var usageGradientColor: String	dynamic public var usage: [MYNTKit.Mynt.Usage]	//电池	dynamic public var battery: Int	//设备类型	dynamic public var myntType: SCloudKit.SCDeviceType	dynamic public var isActivityTracking: Bool	dynamic public var stepGoal: Int	dynamic public var calGoal: Int	dynamic public var step: Int	dynamic public var cal: Int	public var command: SCloudKit.SCDeviceCommand	dynamic public var workStatus: SCloudKit.SCWorkStatus	dynamic public var simStatus: SCloudKit.SCSIMStatus	dynamic public var simType: SCloudKit.SCSIMType	dynamic public var expiryTime: Int	dynamic public var isArrearage: Bool	dynamic public var isStatic: Bool	dynamic public var canEdit: Bool	dynamic public var isOwner: Bool	dynamic public var myntSyncTime: Int	dynamic public var isShowWillOverdueDialog: Bool	dynamic public var isShowOverduedDialog: Bool	dynamic public var isShowDeactivatedDialog: Bool	dynamic public var isLowPowerMode: Bool	dynamic public var isHIDMode: Bool	dynamic public var isEnableControl: Bool	dynamic public var control: SCloudKit.SCControlMode	dynamic public var controls: [MYNTKit.Mynt.Control]	dynamic public var isOpenActivityAlarm: Bool	dynamic public var activityAlarm: SCloudKit.SCDeviceAlarm	dynamic public var activityAlarmStep: Int	dynamic public var activityAlarmTime: Int	override public var sk_primaryKeys: [String] { get }	override public var sk_ignoreKeys: [String] { get }	dynamic public var isNeverShowUpdateFirmware: Bool	dynamic public var avatar: UIImage?	public var state: MYNTState { get }	public var isAlarm: Bool { get }	dynamic public var totallyAddress: String	dynamic public var simplifyAddress: String	dynamic public var coordinate: CLLocationCoordinate2D	public var ignoreKVOKeys: [String] { get }	public var addKVOKeys: [String] { get }	weak public var stMynt: STMynt?	public var hardwareType: MYNTHardwareType { get }	public var needAlarmWhenDisconnect: Bool	required public init()	override public func observeValue(forKeyPath keyPath: String?, of object: Any?, change: [NSKeyValueChangeKey : Any]?, context: UnsafeMutableRawPointer?)}extension Mynt {		public class Control : SlightechKit.SKSQLiteModel {		public var name: String		public var value: SCloudKit.SCControlMode		public var sn: String		public var click: SCloudKit.SCClickValue		public var doubleClick: SCloudKit.SCClickValue		public var tripleClick: SCloudKit.SCClickValue		public var hold: SCloudKit.SCClickValue		public var clickHold: SCloudKit.SCClickValue		override public var sk_primaryKeys: [String] { get }		override public var sk_tableName: String { get }		public func equals(_ control: MYNTKit.Mynt.Control) -> Bool	}}extension Mynt {		public class Usage : SlightechKit.SKSQLiteModel {		public var name: String		public var value: SCloudKit.SCDeviceUsage		public var sn: String		public var phoneAlarm: SCloudKit.SCDeviceAlarm		public var myntAlarm: SCloudKit.SCDeviceAlarm		public var sensitivity: SCloudKit.SCSensitivity		public var locationFrequency: SCloudKit.SCLocationFrequency		override public var sk_primaryKeys: [String] { get }		override public var sk_tableName: String { get }		public func equals(_ usageValue: MYNTKit.Mynt.Usage) -> Bool 	}}extension Mynt {		/**	 * 下载步数记录	 *	 * @param start 开始时间	 * @param end   结束时间	 */	public func downStepLocations(start: Int = default, end: Int = default, success: (([SCloudKit.SCDevice.SCLocation]) -> Swift.Void)? =		default, failure: MyntFailureHandler)	/**	 * 下载运动数据	 *	 * @param start 开始时间	 * @param end   开始时间	 */	public func downloadActivityInfo(start: Int = default, end: Int = default, success: MyntSuccessHandler = default, failure: MyntFailureHandler)	/**	 * 更新运动目标	 *	 * @param exerciseGoal 目标数量	 */	public func uploadStepGoal(stepGoal: Int, success: MyntSuccessHandler, failure: MyntFailureHandler)	/**	 * 设置运动报警	 *	 * @param isOpenActivityAlarm 无活动报警开关	 * @param activityAlarm 	  无活动报警类型	 * @param activityAlarmStep   无活动报警步数	 * @param activityAlarmTime   无活动报警时间	 */	public func uploadActivityAlarm(isOpenActivityAlarm: Bool? = default, activityAlarm: SCloudKit.SCDeviceAlarm? = default, activityAlarmStep:		Int? = default, activityAlarmTime: Int? = default, success: MyntSuccessHandler, failure: MyntFailureHandler)}extension Mynt {		public enum BindState : Int {		case none		case connecting		case binding		case connected		case disconnected	}	public var rssi: Int { get }	/**		初次绑定		*/	public func bind(handler: (((MYNTKit.Mynt, MYNTKit.Mynt.BindState, String?) -> Swift.Void)?)	/**	 	连接	 	*/	public func disconnect()	/**	 	查找小觅	 	*/	public func findMynt()	public func updateFirmware(start: (() -> Data?)?, progress: ((CGFloat) -> Swift.Void)?, success: (() -> Swift.Void)?, failure: ((Error?) -> Swift.Void)?)	public func writeMotionSensibility(sensitivity: Int = default, handler: ((Error?) -> Swift.Void)? = default)	public func writeDBM(dbm: Int = default, handler: ((Error?) -> Swift.Void)? = default)	public func readICCID(isIgnoreTime: Bool = default, handler: ((String?) -> Swift.Void)? = default)	/**		读取电量		*/	public func readBattery()	/**		设备关机		*/	public func shutdown()	/**		设备重启		*/	public func startup()	/**		设置apn		*/	public func setAPN(apn: String, handler: ((Error?) -> Swift.Void)?)}extension Mynt {		public func startEduFindMynt(_ block: ((MYNTKit.Mynt) -> Swift.Void)?)	public func stopEduFindMynt()	public func startEduFindPhone(_ block: ((MYNTKit.Mynt) -> Swift.Void)?)	public func stopEduFindPhone()}