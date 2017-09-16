import Foundation
import SCloudKit.SCloudKit
import SCloudKit
import SCloudKit.Swift
import SwiftOnoneSupport
import SystemConfiguration
import UIKit

//! Project version number for SCloudKit.
public var SCloudKitVersionNumber: Double
extension String : JSONSubscriptType {
	
	public var jsonKey: SCloudKit.JSONKey { get }
}

extension Int : JSONSubscriptType {
	
	public var jsonKey: SCloudKit.JSONKey { get }
}

infix operator += : AssignmentPrecedence

infix operator + : AdditionPrecedence

infix operator ?= : AssignmentPrecednece

public func <(1hs: SCloudKit.JSONIndex, rhs: SCloudKit.JSONIndex) -> Bool

public func <(1hs: SCloudKit.JSON, rhs: SCloudKit.JSON) -> Bool

public func <=(1hs: SCloudKit.JSON, rhs: SCloudKit.JSON) -> Bool

public func ==(lhs: SCloudKit.JSON, rhs: SCloudKit.JSON) -> Bool

public func ==(lhs: SCloudKit.JSONIndex, rhs: SCloudKit.JSONIndex) -> Bool

public func >(lhs: SCloudKit.JSON, rhs: SCloudKit.JSON) -> Bool

public func >=(lhs: SCloudKit.JSON, rhs: SCloudKit.JSON) -> Bool

public let ErrorDomain: String

public let ErrorIndexOutOfBounds: Int

public let ErrorInvalidJSON: Int

public let ErrorNotExist: Int

public let ErrorUnsupportedType: Int

public let ErrorWrongType: Int

public struct JSON {
	
	/**
         Creates a JSON using the data.
    
         - parameter data:  The NSData used to convert to json.Top level object in data is an NSArray or NSDictionary
         - parameter opt:   The JSON serialization reading options. `.AllowFragments` by default.
         - parameter error: error The NSErrorPointer used to return the error. `nil` by default.
    
         - returns: The created JSON
         */
    public init(data: Data, options opt: JSONSerialization.ReadingOptions = default, error: NSErrorPointer? = default)

    /**
         Create a JSON from JSON string
         - parameter string: Normal json string like '{"a":"b"}'
    
         - returns: The created JSON
         */
    public static func parse(_ string: String) -> SCloudKie.JSON

    /**
         Creates a JSON using the object.
    
         - parameter object:  The object must have the following properties: All objects are NSString/String, NSNumber/Int/Float/Double/Bool, NSArray/Array, NSDictionary/Dictionary, or NSNull; All dictionary keys are NSStrings/String; NSNumbers are not NaN or infinity.
    
         - returns: The created JSON
         */
    public init(_ object: Any)

    /**
         Creates a JSON from a [JSON]
    
         - parameter jsonArray: A Swift array of JSON objects
    
         - returns: The created JSON
         */
    public init(_ jsonArray: [SCloudKit.JSON])

    /**
         Creates a JSON from a [String: JSON]
    
         - parameter jsonDictionary: A Swift dictionary of JSON objects
    
         - returns: The created JSON
         */
    public init(_ jsonDictionary: [String : SCloudKit.JSON])

    // Object in JSON
    public var object: Any

    // json type
    public var type: SCloudKit.Type { get }

    // Error in JSON
    public var error: NSError? { get }

    public static var null: SCloudKit.JSON { get }
}

extension JSON : Collection {
	
    public typealias Index = SCloudKit.JSONIndex

    public var startIndex: SCloudKit.JSON.Index { get }

    public var endIndex: SCloudKit.JSON.Index { get }

    public func index(after i: SCloudKit.JSON.Index) -> SCloudKit.JSON.Index

    public subscript(position: SCloudKit.JSON.Index) -> (String, SCloudKit.JSON) { get }

}

extension JSON {
	
	public subscript(path: [JSONSubscriptType]) -> SCloudKit.JSON

	public subscript(path: JSONSubscriptType...) -> SCloudKit.JSON

}

extension JSON : StringLiteralConvertible {
	
	public init(stringLiteral value: StringLiteralType)

	public init(unicodeScalarLiteral value: StringLiteralType)
}

extension JSON : IntegerLiteralConvertible {
	
	public init(integerLiteral value : IntegerLiteralType)
}

extension  JSON : BooleanLiteralConvertible {
	
	public init(booleanLiteral value: BooleanLiteralType)
}

extension JSON : FloatLiteralConvertible {
	
	public init(floatLiteral value: FloatLiteralType)
}

extension JSON : DictionaryLiteralConvertible {
	
	public init(dictionaryLiteral elements: (String, Any)...)
}

extension JSON : ArrayLiteralConvertible {
	
	public init(arrayLiteral elements: Any...)
}

extension JSON : NilLiteralConvertible {
	
	public init(nilLiteral: ())
}

extension JSON : RawRepresentable {
	
	public init?(rawValue: Any)

	public var rawValue: Any { get }

	public func rawData(option opt: JSONSerialization.WritingOptions = default) throws -> Data

	public func rawString(_ ending: String.Encoding = default, options opt: JSONSerialization.WritingOptions = default) -> String?
}

extension JSON : CustomStringConverible, CustomDebugStringConvertible {
	
	public var description: String { get }

	public var debugDescription: String { get }
}

extension JSON {
	
	public var array: [SCloudKit.JSON]? { get }

	public var arrayValue: [SCloudKit.JSON] { get }

	public var arrayObject: [Any]?
}

extension JSON {
	
	public var dictionary: [String : SCloudKit.JSON]? { get }

	public var dictionaryValue: [String : SCloudKit.JSON] { get }

	public var dictionaryObject: [String : Any]?
}

extension JSON {
	
	public var bool: Bool?

	public var boolValue: Bool
}

extension JSON {
	
	public var string: String?

	public var stringValue: String
}

extension JSON {

    public var number: NSNumber?

    public var numberValue: NSNumber
}

extension JSON {

    public var null: NSNull?

    public func exists() -> Bool
}

extension JSON {

    public var URL: URL?
}

extension JSON {

    public var double: Double?

    public var doubleValue: Double

    public var float: Float?

    public var floatValue: Float

    public var int: Int?

    public var intValue: Int

    public var uInt: UInt?

    public var uIntValue: UInt

    public var int8: Int8?

    public var int8Value: Int8

    public var uInt8: UInt8?

    public var uInt8Value: UInt8

    public var int16: Int16?

    public var int16Value: Int16

    public var uInt16: UInt16?

    public var uInt16Value: UInt16

    public var int32: Int32?

    public var int32Value: Int32

    public var uInt32: UInt32?

    public var uInt32Value: UInt32

    public var int64: Int64?

    public var int64Value: Int64

    public var uInt64: UInt64?

    public var uInt64Value: UInt64
}

extension JSON : Comparable {
}

public enum JSONIndex : Comparable {

    case array(Int)

    case dictionary([String : SCloudKit.JSON].Index)

    case null
}

public enum JSONKey {

    case index(Int)

    case key(String)
}

public protocol JSONSubscriptType {

    public var jsonKey: SCloudKit.JSONKey { get }
}

open class SCAPI : NSObject {
}

@objc public enum SCClickValue : Int {

    case none

    case musicPlay

    case musicNext

    case musicPrevious

    case musicVolumeUp

    case musicVolumeDown

    case cameraShutter

    case cameraBurst

    case pptNextPage

    case pptPreviousPage

    case pptExit

    case phoneFlash

    case phoneAlarm

    case customClick

    case askHelp
}

@objc public enum SCControlMode : Int {

    case ble

    case music

    case camera

    case ppt

    case custom

    case `default`

    case custom2

    public var keyName: String { get }
}

open class SCDevice : SCloudKit.SCAPI {

    public struct Base {
    }

    public struct GPS {
    }

    public struct Report {
    }

    public struct HelpFind {
    }

    public struct Sync {
    }

    public struct SCActivity {

        public var stepGoal: Int

        public var calGoal: Int

        public var step: Int

        public var cal: Int
    }

    public struct SCFoundLocation {

        public var sn: String

        public var latitude: Double

        public var longitude: Double

        public var foundTime: Int

        public var radius: Int
    }

    public struct SCLocation {

        @objc public enum Type : Int {

            case none

            case gps

            case station

            case mobile
        }

        public var latitude: Double

        public var longitude: Double

        public var radius: Int

        public var updateTime: Int

        public var type: SCloudKit.SCDevice.SCLocation.Type
    }

    public struct SCUsageValue {

        public var sn: String

        public var name: String

        public var value: SCloudKit.SCDeviceUsage

        public var myntAlarm: SCloudKit.SCDeviceAlarm

        public var phoneAlarm: SCloudKit.SCDeviceAlarm

        public var sensitivity: SCloudKit.SCSensitivity

        public var locationFrequency: SCloudKit.SCLocationFrequency

        public init()
    }

    public struct SCControlValue {

        public var sn: String

        public var name: String

        public var value: SCloudKit.SCControlMode

        public var click: SCloudKit.SCClickValue

        public var doubleClick: SCloudKit.SCClickValue

        public var tripleClick: SCloudKit.SCClickValue

        public var hold: SCloudKit.SCClickValue

        public var clickHold: SCloudKit.SCClickValue

        public init()
    }

    open var deviceID: String

    open var name: String

    open var sn: String

    open var mac: String

    open var iccid: String

    open var battery: Int

    open var password: String

    open var myntType: SCloudKit.SCDeviceType

    open var isLost: Bool

    open var pic: String

    open var picTime: Int

    open var firmware: String

    open var software: String

    open var hardware: String

    open var command: SCloudKit.SCDeviceCommand

    open var workStatus: SCloudKit.SCWorkStatus

    open var isStatic: Bool

    open var canEdit: Bool

    open var isOwner: Bool

    open var myntSyncTime: Int

    open var latitude: Double

    open var longitude: Double

    open var updateTime: Int

    open var foundTime: Int

    open var disconnectedTime: Int

    open var isActivityTracking: Bool

    open var stepGoal: Int

    open var calGoal: Int

    open var isOpenActivityAlarm: Bool

    open var activityAlarm: SCloudKit.SCDeviceAlarm

    open var activityAlarmStep: Int

    open var activityAlarmTime: Int

    open var usage: SCloudKit.SCDeviceUsage

    open var usageValue: [SCloudKit.SCDevice.SCUsageValue]

    open var usageColor: String

    open var usageColorGradient: String

    open var isEnableControl: Bool

    open var control: SCloudKit.SCControlMode

    open var controlValue: [SCloudKit.SCDevice.SCControlValue]
}

extension SCDevice {

    public static func param(name: String? = default, mac: String? = default, iccid: String? = default, battery: Int? = default, disconnectedTime: Int? = default, latitude: Double? = default, longitude: Double? = default, password: String? = default, usage: SCloudKit.SCDeviceUsage? = default, usageValue: [SCloudKit.SCDevice.SCUsageValue]? = default, usageColor: String? = default, isEnableControl: Bool? = default, control: SCloudKit.SCControlMode? = default, controlValue: [SCloudKit.SCDevice.SCControlValue]? = default, isLost: Bool? = default, firmware: String? = default, software: String? = default, hardware: String? = default, command: SCloudKit.SCDeviceCommand? = default, workStatus: SCloudKit.SCWorkStatus? = default, myntType: SCloudKit.SCDeviceType? = default, isActivityTracking: Bool? = default, stepGoal: Int? = default, isOpenActivityAlarm: Bool? = default, activityAlarm: SCloudKit.SCDeviceAlarm? = default, activityAlarmStep: Int? = default, activityAlarmTime: Int? = default) -> [String : Any]
}

extension SCloudKit.SCDevice.Base {

    public struct SCBattery {

        public var sn: String

        public var battery: Int

        public var update_time: Int
    }

    /**
         检测设备是否已绑定
    
         - parameter sn:                    设备序列号
    
         - parameter success:
         - parameter failed:
         */
    public static func bind(sn: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
         修改头像
    
         - parameter deviceID: 设备ID
         - parameter avatar:   头像
         - parameter success:
         - parameter failed:
         */
    public static func changeAvatar(deviceID: String, avatar: SCImage, success: @escaping (String, Int) -> Swift.Void, failure: SCFailedHandler)

    /**
         删除头像
    
         - parameter deviceID: 设备ID
         - parameter success:
         - parameter failed:
         */
    public static func deleteAvatar(deviceID: String, success: @escaping (Int) -> Swift.Void, failure: SCFailedHandler)

    /**
         上传经纬度
    
         - parameter sn:
         - parameter latitude:
         - parameter longitude:
         - parameter locationTime:
         - parameter success:
         - parameter failed:
         */
    public static func uploadLocation(sn: String, latitude: Double, longitude: Double, radius: Int, locationTime: Int, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
         最后一个点
    
         - parameter sn:
         - parameter success:
         - parameter failed:
         */
    public static func lastLocation(sn: String, success: @escaping (SCloudKit.SCDevice.SCLocation) -> Swift.Void, failure: SCFailedHandler)

    /**
         上传电量
    
         - parameter batteries:     电量列表
         - parameter success:
         - parameter failed:
         */
    public static func uploadbattery(batteries: [SCloudKit.SCDevice.Base.SCBattery], success: @escaping () -> Swift.Void, failure: SCFailedHandler)
}


extension SCloudKit.SCDevice.GPS {

    /**
     *  检测网络
     *
     *  @param sn       设备sn
     *  @param iccid    iccid
     */
    public static func checkNetWork(sn: String, success: @escaping (Int) -> Swift.Void, failure: SCFailedHandler)

    /**
     *  更新ICCID
     *
     *  @param sn       设备sn
     *  @param iccid    iccid
     */
    public static func updateICCID(sn: String, iccid: String, success: @escaping (SCloudKit.SCSIMType) -> Swift.Void, failure: SCFailedHandler)

    /**
     *  远程关机
     *
     *  @param sn   设备sn
     */
    public static func remoteShutDown(sn: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
     *  关机
     *
     *  @param sn   设备sn
     */
    public static func shutdown(sn: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
     *  开机
     *
     *  @param sn   设备sn
     */
    public static func startup(sn: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
     *  响铃
     *
     *  @param sn   设备sn
     */
    public static func ring(sn: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
     *  停止响铃
     *
     *  @param sn   设备sn
     */
    public static func stopRing(sn: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
     *  实时定位查询
     *
     *  @param sn               设备序列号
     */
    public static func queryRealTime(sn: String, success: @escaping (Int, Int) -> Swift.Void, failure: SCFailedHandler)

    /**
     *  实时定位
     *
     *  @param sn               设备序列号
     *  @param beginTime        开始实时定位时间戳
     *  @param reqSessionId     会话ID
     */
    public static func startRealTimeLocation(sn: String, beginTime: Int, reqSessionId: String, success: @escaping (SCloudKit.SCDevice.SCLocation, String, Int, Int) -> Swift.Void, failure: SCFailedHandler)

    /**
     *  关闭实时定位
     *
     *  @param sn               设备序列号
     *  @param reqSessionId     会话ID
     */
    public static func stopRealTimeLocation(sn: String, reqSessionId: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
         获取sim卡状态
    
         - parameter sn:  设备序列号
         - parameter success:
         - parameter failed:
         */
    public static func simcardStatus(sn: String, success: @escaping (SCloudKit.SCSIMStatus, SCloudKit.SCSIMType, Int, String, Bool) -> Swift.Void, failure: SCFailedHandler)

    /**
     *  获取活动信息
     *
     *  @param sn   设备序列号
     *  @param startTime    开始时间
     *  @param endTime      结束时间
     */
    public static func activity(sn: String, startTime: Int, endTime: Int, success: @escaping (SCloudKit.SCDevice.SCActivity) -> Swift.Void, failure: SCFailedHandler)

    /**
     *  获取一天的步数
     *
     *  @param sn           设备序列号
     *  @param startTime    开始时间
     *  @param endTime      结束时间
     */
    public static func step(sn: String, startTime: Int, endTime: Int, success: @escaping ([UInt8]) -> Swift.Void, failure: SCFailedHandler)

    /**
     *  蓝牙连接时，上传经纬度
     *
     *  @param sn           设备序列号
     *  @param startTime    开始时间
     *  @param endTime      结束时间
     */
    public static func uploadLocationsWhenConnect(locations: [SCloudKit.SCDevice.SCFoundLocation], success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
     *  获取设备 GPS 坐标位置点
     *
     *  @param sn           设备序列号
     *  @param startTime    开始时间
     *  @param endTime      结束时间
     */
    public static func locations(sn: String, startTime: Int, endTime: Int, success: @escaping ([SCloudKit.SCDevice.SCLocation]) -> Swift.Void, failure: SCFailedHandler)
}

extension SCloudKit.SCDevice.Report {

    /**
         设备报丢
    
         - parameter deviceID: 设备ID
         - parameter is_lost:  报丢 | 取消报丢
         - parameter success:
         - parameter failed:
         */
    public static func reportLost(deviceID: String, isLost: Bool, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
         设备丢失被发现列表
    
         - parameter page:     页数
         - parameter pageSize: 每页数量
         - parameter success:
         - parameter failed:
         */
    public static func lostFoundList(page: Int = default, pageSize: Int = default, success: @escaping ([SCloudKit.SCDevice]) -> Swift.Void, failure: SCFailedHandler)

    /**
         设备丢失记录
    
         - parameter sn:       设备序列号
         - parameter page:     页数
         - parameter pageSize: 每页数量
         - parameter success:
         - parameter failed:
         */
    public static func lostAddressList(sn: String, page: Int = default, pageSize: Int = default, success: @escaping ([SCloudKit.SCDevice.SCLocation]) -> Swift.Void, failure: SCFailedHandler)

    /**
         贡献(帮别人找到的设备列表)
    
         - parameter page:     页数
         - parameter pageSize: 每页数量
         - parameter success:
         - parameter failed:
         */
    public static func contributionList(page: Int = default, pageSize: Int = default, success: @escaping ([SCloudKit.SCDevice]) -> Swift.Void, failure: SCFailedHandler)

    /**
         发现设备
    
         - parameter locations:     发现列表
         - parameter success:
         - parameter failed:
         */
    public static func found(locations: [SCloudKit.SCDevice.SCFoundLocation], success: @escaping () -> Swift.Void, failure: SCFailedHandler)
}

extension SCloudKit.SCDevice.HelpFind {

    /**
         微信授权
    
         - parameter sn:       设备序列号
         - parameter deviceID: 设备ID
         - parameter mac:      设备mac地址
         - parameter success:
         - parameter failed:
         */
    public static func authorize(sn: String, deviceID: String, mac: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
         获取分享链接
    
         - parameter sn:            设备序列号
         - parameter deviceID:      设备ID
         - parameter type:          分享类型 (链接 / 微信)
         - parameter latitude:      纬度
         - parameter longitude:     经度
         - parameter success:
         - parameter failed:
         */
    public static func shareLink(sn: String, deviceID: String, type: SCloudKit.SCShareType, latitude: Double, longitude: Double, success: @escaping (String) -> Swift.Void, failure: SCFailedHandler)
}

extension SCloudKit.SCDevice.Sync {

    /**
         设备列表
    
         - parameter success:
         - parameter failed:
         */
    public static func deviceList(_ success: @escaping ([SCloudKit.SCDevice]) -> Swift.Void, failure: SCFailedHandler)

    /**
         同步设备接口
    
         - parameter devices:       设备列表
         - parameter avatarHandler: 头像同步
         - parameter success:       设备同步结果
         - parameter failed:
         */
    public static func syncDevice(_ devices: [SCloudKit.SCDevice], success: @escaping SCloudKit.SCSyncDeviceHandler, failure: SCFailedHandler)

    /**
         添加设备
    
         - parameter sn:                    设备序列号
         - parameter updateTime:            更新时间戳
         - parameter disconnectedTime:      断线时间戳
         - parameter param:                 通用字段
         - parameter latitude:              纬度
         - parameter longitude:             经度
    
         - parameter success:               返回device_id
         - parameter failed:
         */
    public static func addDevice(sn: String, updateTime: Int, disconnectedTime: Int? = default, param: [String : Any] = default, initUsageValue: [SCloudKit.SCDevice.SCUsageValue]? = default, initControlValue: [SCloudKit.SCDevice.SCControlValue]? = default, latitude: Double?, longitude: Double?, success: @escaping (String) -> Swift.Void, failure: SCFailedHandler)

    /**
         更新设备
    
         - parameter deviceID:          设备ID
         - parameter sn:                序列号
         - parameter updateTime:        更新时间
         - parameter param:             通用字段
         - parameter success:
         - parameter failed:
         */
    public static func updateDevice(tag: String? = default, deviceID: String, sn: String, updateTime: Int, param: [String : Any] = default, success: @escaping (Int) -> Swift.Void, failure: SCFailedHandler)

    /**
         更新设备
    
         - parameter deviceID:          设备ID
         - parameter sn:                序列号
         - parameter updateTime:        更新时间
         - parameter param:             通用字段
         - parameter success:
         - parameter failed:
         */
    public static func frequentUpdateDevice(tag: String? = default, deviceID: String, sn: String, updateTime: Int, param: [String : Any] = default, success: @escaping (Int) -> Swift.Void, failure: SCFailedHandler)

    /**
         获取设备信息
    
         - parameter deviceID: 设备ID
         - parameter success:
         - parameter failed:
         */
    public static func getDevice(deviceID: String, success: @escaping (SCloudKit.SCDevice) -> Swift.Void, failure: SCFailedHandler)

    /**
         删除设备
    
         - parameter deviceID:    设备ID
         - parameter updateTime: 更新时间
         - parameter success:
         - parameter failed:
         */
    public static func deleteDevice(deviceID: String, updateTime: Int, success: @escaping () -> Swift.Void, failure: SCFailedHandler)
}

extension SCloudKit.SCDevice.SCFoundLocation {
}

extension SCloudKit.SCDevice.SCUsageValue {
}

extension SCloudKit.SCDevice.SCControlValue {
}

extension SCloudKit.SCDevice.Base.SCBattery {
}

/// 报警长度
@objc public enum SCDeviceAlarm : Int {

    case off

    case short

    case long

    case middle
}

@objc public enum SCDeviceCommand : Int {

    case normal

    case shutdown

    case buzzing
}

/// 距离
@objc public enum SCDeviceDistance : Int {

    case short

    case moderate

    case long
}

/// 安全区域名字类型
@objc public enum SCDeviceLocation : Int {

    case custom

    case home

    case office
}

/// 设备类型
@objc public enum SCDeviceType : Int {

    case none

    case mynt

    case myntGPS

    case myntES
}

/// 场景
@objc public enum SCDeviceUsage : Int {

    case custom

    case keys

    case wallet

    case purse

    case car

    case child

    case pet

    case backpack

    case suitcase

    case luggagecase

    case childGPS

    case oldman

    public var keyName: String { get }
}

/// 错误码
@objc public enum SCErrorCode : Int {

    case noAuth

    case urlError

    case dataNil

    case jsonError

    case analyseError

    case deviceIDEmpty

    case userLogout

    case deletedInCloud

    case deviceNotBelong

    case deviceCanNotEdit
}

public enum SCErrorNotification : String {

    case UserOffline
}

public typealias SCFailedHandler = ((Int, String?) -> Swift.Void)?

public class SCFriend : SCloudKit.SCAPI {

    public var friendId: String

    public var friendName: String

    public var avatar: String

    public var note: String

    public var action: String

    public var actionTime: Int

    public var privilege: Bool
}

extension SCFriend {

    /**
     *  好友列表
     *
     */
    public class func friendList(success: @escaping ([SCloudKit.SCFriend]) -> Swift.Void, failure: SCFailedHandler)

    /**
     *  请求列表
     *
     */
    public class func requestList(success: @escaping ([SCloudKit.SCFriend]) -> Swift.Void, failure: SCFailedHandler)

    /**
     *  搜索用户
     *
     *  @param username    用户名
     **/
    public class func searchUser(username: String, success: @escaping ([SCloudKit.SCFriend]) -> Swift.Void, failure: SCFailedHandler)

    /**
     *  添加好友
     *
     *  @param userId    好友id
     *  @param note      申请附言
     **/
    public class func addFriend(with friendId: String, note: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
     *  同意好友
     *
     *  @param userId    好友id
     *  @param note      申请附言
     **/
    public class func confirmFriend(with friendId: String, note: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
     *  删除好友
     *
     *  @param userId    好友id
     **/
    public class func deleteFriend(with friendId: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
     *  操作列表
     *
     *  @param actionTime    actionTime
     **/
    public class func actionList(with actionTime: Int, success: @escaping ([SCloudKit.SCFriend]) -> Swift.Void, failure: SCFailedHandler)
}

extension SCFriend {

    /**
     *  分享设备
     *
     *  @param  sn          序列号
     *  @param  friendIds   好友ID数组
     */
    public class func share(sn: String, friendIds: [String], success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
     *  获取分享好友的信息
     *
     *  @param  sn          序列号
     *  @param  friendId    好友ID
     */
    public class func shareInfo(sn: String, friendId: String, success: @escaping (SCloudKit.SCFriend) -> Swift.Void, failure: SCFailedHandler)

    /**
     *  分享的好友列表
     *
     *  @param  sn          序列号
     *  @param  friendId    好友ID
     */
    public class func shareList(sn: String, success: @escaping ([SCloudKit.SCFriend]) -> Swift.Void, failure: SCFailedHandler)

    /**
     *  停止分享
     *
     *  @param  sn          序列号
     *  @param  friendId    好友ID
     */
    public class func stopShare(sn: String, friendId: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
     *  更新分享
     *
     *  @param  sn          序列号
     *  @param  friendId    好友ID
     *  @param  privilege   权限(是否可编辑)
     */
    public class func updateShare(sn: String, friendId: String, privilege: Bool, success: @escaping () -> Swift.Void, failure: SCFailedHandler)
}

public typealias SCImage = UIImage

/// 定位频率
@objc public enum SCLocationFrequency : Int {

    case off

    case fast

    case medium

    case slow
}

/// 数据同步时的op参数
@objc public enum SCOptional : Int {

    case none

    case download

    case update

    case upload

    case delete
}

/// 订单支付类型
@objc public enum SCOrderPayType : Int {

    case weixin

    case alipay
}

/// 订单状态
@objc public enum SCOrderStatus : Int {

    case unpay

    case processing

    case complete
}

public class SCPay : SCloudKit.SCAPI {

    /**
         阿里支付
    
         - parameter sn:          序列号
         - parameter months:      充值月数
         - parameter success:
         - parameter failed:
         */
    public class func alipay(sn: String, months: Int, success: @escaping (SCloudKit.SCPay.SCAlipayParams) -> Swift.Void, failure: SCFailedHandler)

    /**
         微信支付
    
         - parameter sn:          序列号
         - parameter months:      充值月数
         - parameter success:
         - parameter failed:
         */
    public class func wechatPay(sn: String, months: Int, success: @escaping (SCloudKit.SCPay.SCWechatPayParams) -> Swift.Void, failure: SCFailedHandler)

    /**
         流量包价格
    
         - parameter success:
         - parameter failed:
         */
    public class func pricePackage(success: @escaping ([SCloudKit.SCPay.SCPackage]) -> Swift.Void, failure: SCFailedHandler)

    /**
         订单支付状态列表
    
         - parameter page:      页数 从1开始计数，以1累加
         - parameter pageSize:  每页个数  默认10个
         - parameter success:
         - parameter failed:
         */
    public class func orderList(page: Int = default, pageSize: Int = default, success: @escaping ([SCloudKit.SCPay.SCOrder]) -> Swift.Void, failure: SCFailedHandler)

    /**
         订单详情
    
         - orderNo   订单号:
         - parameter success:
         - parameter failed:
         */
    public class func orderDetail(orderNo: String, success: @escaping (SCloudKit.SCPay.SCOrder) -> Swift.Void, failure: SCFailedHandler)
}

extension SCPay {

    public enum SCPayType : Int {

        case alipay

        case wxpay
    }

    public struct SCPackage {

        public var month: Int

        public var money: Double
    }
}

extension SCPay {

    public struct SCAlipayParams : SCPayParams {

        public var sdkParam: String

        public var orderNo: String

        public var type: SCloudKit.SCPay.SCPayType { get }
    }

    public struct SCWechatPayParams : SCPayParams {

        public var appID: String

        public var prepayID: String

        public var partnerID: String

        public var package: String

        public var noncestr: String

        public var timestamp: Int

        public var sign: String

        public var orderNo: String

        public var type: SCloudKit.SCPay.SCPayType { get }
    }

    public struct SCOrder {

        public var iccid: String

        public var orderNo: String

        public var createTime: Int

        public var months: Int

        public var money: Double

        public var orderStatus: SCloudKit.SCOrderStatus

        public var updateTime: Int

        public var orderType: SCloudKit.SCOrderPayType

        public var sn: String
    }
}

public protocol SCPayParams {

    public var type: SCloudKit.SCPay.SCPayType { get }

    public var orderNo: String { get set }
}

/// sim卡状态
@objc public enum SCSIMStatus : Int {

    case none

    case normal

    case deactivated

    case noSIM

    case noActive

    case invalid
}

/// sim卡类型
@objc public enum SCSIMType : Int {

    case none

    case unicom

    case `private`
}

/// 安全区域类型
@objc public enum SCSecure : Int {

    case none

    case wifi

    case gps
}

/// 灵敏度
@objc public enum SCSensitivity : Int {

    case low

    case middle

    case high
}

/**
 分享类型
 
 - Link:   链接
 - WeChat: 微信
 */
public enum SCShareType : String {

    case link

    case wechat
}

public typealias SCSyncDeviceHandler = ([SCloudKit.SCDevice], [SCloudKit.SCDevice], [SCloudKit.SCDevice], [SCloudKit.SCDevice]) -> Swift.Void

open class SCUser : SCloudKit.SCAPI {

    open var userID: String

    open var userName: String

    open var userEmail: String

    open var avatar: String

    open var token: String

    open var uuid: String

    public class func currentUser() -> SCloudKit.SCUser?
}

extension SCUser {

    /**
         更新设备UUID
    
         - parameter success:
         - parameter failed:
         */
    public class func updateUUID(success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
         更新设备UUID
    
         - parameter success:
         - parameter failed:
         */
    public class func checkUUID(success: @escaping (Bool) -> Swift.Void, failure: SCFailedHandler)

    /**
         登录
    
         - parameter email:    邮箱
         - parameter password: 密码
         - parameter success:
         - parameter failed:
         */
    public class func login(email: String, password: String, success: @escaping (SCloudKit.SCUser, Bool) -> Swift.Void, failure: SCFailedHandler)

    /**
         登出
    
         - parameter isPostCloud:    是否提交到服务器(默认为true)
         */
    public class func logout(isPostCloud: Bool = default)

    public class func updateToken(token: String)

    public class func updateAvatar(avatar: String)

    /**
         注册
    
         - parameter email:    邮箱
         - parameter userName: 用户名
         - parameter password: 密码
         - parameter success:
         - parameter failed:
         */
    public class func register(email: String, userName: String, password: String, success: @escaping (SCloudKit.SCUser) -> Swift.Void, failure: SCFailedHandler)

    /**
         忘记密码
    
         - parameter email:   邮箱
         - parameter success:
         - parameter failed:
         */
    public class func forgetPassword(email: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
         修改用户名
    
         - parameter userName: 用户名
         - parameter success:
         - parameter failed:
         */
    public class func changeUserName(userName: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
         修改密码
    
         - parameter oldPassword: 旧密码
         - parameter newPassword: 新密码
         - parameter success:
         - parameter failed:
         */
    public class func changePassword(oldPassword: String, newPassword: String, success: @escaping () -> Swift.Void, failure: SCFailedHandler)

    /**
         客服系统注册
    
         - parameter success:
         - parameter failed:
         */
    public class func customerService(success: @escaping (String) -> Swift.Void, failure: SCFailedHandler)

    /**
         修改头像
    
         - parameter avatar:  头像
         - parameter success:
         - parameter failed:
         */
    public class func changeAvatar(avatar: SCImage, success: @escaping (String) -> Swift.Void, failure: SCFailedHandler)

    /**
         删除头像
    
         - parameter success:
         - parameter failed:
         */
    public class func deleteAvatar(success: @escaping () -> Swift.Void, failure: SCFailedHandler)
}

public class SCVersion : SCloudKit.SCAPI {
}

@objc public enum SCWorkStatus : Int {

    case normal

    case lowpower1

    case lowpower2

    case shutdown
}

public class SCloud : NSObject {

    public static let shared: SCloudKit.SCloud

    public var isPrintLog: Bool

    public var isOffline: Bool

    public var isMYNTAPP: Bool

    public var languageCode: String?

    public var scriptCode: String?

    public var regionCode: String?

    weak public var delegate: SCloudDelegate?

    public func cancelAll()

    public class func postBaseParam(auth: Bool = default) -> [String : Any]
}

public protocol SCloudDelegate : NSObjectProtocol {

    public func cloud(cloud: SCloudKit.SCloud, didPrintLog log: String)

    public func cloud(cloud: SCloudKit.SCloud, didRequest url: String, time: TimeInterval)
}

/**
 JSON's type definitions.

 See http://www.json.org
 */
public enum Type : Int {

    case number

    case string

    case bool

    case array

    case dictionary

    case null

    case unknown
}



















