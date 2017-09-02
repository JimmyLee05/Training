#import "STMynt.h"
#import "STPeripheral.h"
#import "STCenterManager.h"
#import "STConnectionParams.h"

// MARK: - STMynt
@interface STMynt () <STPeriphrealDelegate>

@property (nonatomic, weak) STPeripheral *peripheral;

@property (nonatomic, strong) NSString *uuid;

@end

@implementation STMynt

- (instancetype)initWithPeripheral: (STPeripheral *)peripheral {
	self = [super init];
	if (self) {
		self.peripheral = peripheral;
	}
	return self;
}

- (instancetype)init NS_UNAVAILABLE {
	self = [super init];
	if (self) {

	}
	return self;
}

- (void)setPeripheral:(STPeripheral *)peripheral {
	_peripheral = peripheral;
	_peripheral.peripheralDelegate = self:
	_uuid = peripheral.uuid;	
}

- (NSString *)name {
		return self.peripheral.peripheral.name;
}

- (NSInteger)RSSI {
		return self.peripheral.RSSI;
}

- (NSInteger)battery {
		return _peripheral.battery;
}

- (MYNTHardwareType)hardwareType {
	return self.peripheral.hardwareType;
}

- (MYNTState)state {
	return _peripheral.logicConnectState;
}

- (BOOL)isAlarm {
	return _peripheral.isAlarm;
}

- (BOOL)isHIDMode {
		return _peripheral.isHIDMode;
}

- (MYNTClickValue)click {
	return _peripheral.click;
}

- (MYNTClickValue)doubleClick {
	return _peripheral.doubleClick;
}

- (MYNTClickValue)tripleClick {
	return _peripheral.tripleClick;
}

- (MYNTClickValue)hold {
	return _peripheral.hold;
}

- (MYNTClickValue)clickHold {
    return _peripheral.clickHold;
}

- (NSString *)manufaturer {
    return _peripheral.manufaturer;
}

- (NSString *)model {
    return _peripheral.model;
}

- (NSString *)firmware {
    return _peripheral.firmware;
}

- (NSString *)hardware {
    return _peripheral.hardware;
}

- (NSString *)software {
    return _peripheral.software;
}

- (NSString *)sn {
    return _peripheral.sn;
}

- (NSString *)mac {
    return _peripheral.mac;
}

// MARK: ==================STPeripheralDelegate==================

- (void)didStartConnect:(STPeripheral *)peripheral {
    if (_delegate && [_delegate respondsToSelector:@selector(myntDidStartConnect:)]) {
        [_delegate myntDidStartConnect:self];
    }
}

- (void)didConnected:(STPeripheral *)peripheral {
    if (_delegate && [_delegate respondsToSelector:@selector(myntDidConnected:)]) {
        [_delegate myntDidConnected:self];
    }
}

- (void)peripheral:(STPeripheral *)peripheral didDisconnected:(NSError *)error {
    if (_delegate && [_delegate respondsToSelector:@selector(mynt:didDisconnected:)]) {
        [_delegate mynt:self didDisconnected:error];
    }
}

- (void)peripheral:(STPeripheral *)peripheral didUpdateBattery:(NSArray<NSNumber *> *)batteries {
    if (_delegate && [_delegate respondsToSelector:@selector(mynt:didUpdateBattery:)]) {
        [_delegate mynt:self didUpdateBattery:batteries];
    }
}


- (void)peripheral:(STPeripheral *)peripheral didUpdateRSSI:(NSInteger)RSSI {
    if (_delegate && [_delegate respondsToSelector:@selector(mynt:didUpdateRSSI:)]) {
        [_delegate mynt:self didUpdateRSSI:RSSI];
    }
}

- (void)peripheral:(STPeripheral *)peripheral didUpdateAlarmState:(BOOL)isAlarm {
    if (_delegate && [_delegate respondsToSelector:@selector(mynt:didUpdateAlarmState:)]) {
        [_delegate mynt:self didUpdateAlarmState:isAlarm];
    }
}

- (void)peripheral:(STPeripheral *)peripheral didReceiveClickEvent:(MYNTClickEvent)clickEvent {
    if (_delegate && [_delegate respondsToSelector:@selector(mynt:didReceiveClickEvent:)]) {
        [_delegate mynt:self didReceiveClickEvent:clickEvent];
    }
}

- (BOOL)didRequestAutoconnect:(STPeripheral *)peripheral {
    if (_delegate && [_delegate respondsToSelector:@selector(didRequestAutoconnect:)]) {
        return [_delegate didRequestAutoconnect:self];
    }
    return NO;
}


- (void)didNeedRestartBluetooth:(STPeripheral * _Nonnull)peripheral {
    if (_delegate && [_delegate respondsToSelector:@selector(didNeedRestartBluetooth:)]) {
        [_delegate didNeedRestartBluetooth:self];
    }
}

// MARK: - ---- 私有回调 ----

- (void)didStartPair:(STPeripheral *)peripheral {
    if (_delegate && [_delegate respondsToSelector:@selector(didStartPair:)]) {
        [_delegate didStartPair:self];
    }
}

- (void)peripheral:(STPeripheral *)peripheral didPairError:(NSError *)error {
    if (_delegate && [_delegate respondsToSelector:@selector(mynt:didPairError:)]) {
        [_delegate mynt:self didPairError:error];
    }
}

- (void)peripheral:(STPeripheral *)peripheral didUpdatePassword:(NSString *)password {
    if (_delegate && [_delegate respondsToSelector:@selector(mynt:didUpdatePassword:)]) {
        [_delegate mynt:self didUpdatePassword:password];
    }
}

- (NSString *)didRequestPassword:(STPeripheral *)peripheral {
    if (_delegate && [_delegate respondsToSelector:@selector(didRequestPassword:)]) {
        return [_delegate didRequestPassword:self];
    }
    return nil;
}

- (void)didSendBluetoothHeartbeat:(STPeripheral *)peripheral {
    [[NSNotificationCenter defaultCenter] postNotificationName:@"STMNYNT_CONNECTTING_HEARTBEAT" object:self];
}

// MARK: ==================Function==================

- (void)connect {
    [_peripheral connect];
}

- (void)disconnect {
    [_peripheral cancelConnection];
}

- (void)toggleAlarm:(BOOL)alarm handler:(void (^ _Nullable)(NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    [_peripheral.alarmService toggleAlarm:alarm handler:handler];
}

- (void)updateFirmware:(NSData * _Nullable (^)())start
              progress:(void (^)(CGFloat))progress
               success:(void (^)())success
               failure:(void (^)(NSError *))failure {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (failure) { failure(ERROR_DISCONNECTED); }
        return;
    }
    switch (_peripheral.hardwareType) {
        case MYNTHardwareTypeMYNTV1:
        case MYNTHardwareTypeMYNTV2:
        case MYNTHardwareTypeMYNTGPS:
            [_peripheral.tiOADService updateFirmware:start progressBlock:progress successBlock:success failedBlock:failure];
            break;
        case MYNTHardwareTypeMYNTES:
            [_peripheral.dialogOADService updateFirmware:start progressBlock:progress successBlock:success failedBlock:failure];
            break;
        default:
            break;
    }
}

- (void)writeAlarmCount:(NSInteger)count
                handler:(void (^ _Nullable)(NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    [_peripheral.alarmService writeAlarmCount:count handler:handler];
}

- (void)writeAlarmDelay:(NSInteger)seconds
                handler:(void (^ _Nullable)(NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    [_peripheral.alarmService writeAlarmDelay:seconds handler:handler];
}

- (void)writeClickValue:(BOOL)isHIDMode
                  click:(MYNTClickValue)click
            doubleClick:(MYNTClickValue)doubleClick
            tripleClick:(MYNTClickValue)tripleClick
                   hold:(MYNTClickValue)hold
              clickHold:(MYNTClickValue)clickHold
                handler:(void (^ _Nullable)(NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    if (_peripheral.hidService.isExistCharacteristic) {
        [self.peripheral.hidService writeClickValue:click doubleClick:doubleClick tripleClick:tripleClick hold:hold clickHold:clickHold handler:handler];
        if (isHIDMode) {
            [self.peripheral.hidService switchHIDMode];
        } else {
            [self.peripheral.hidService switchBLEMode];
        }
    }
    if (_peripheral.instructionService.isExistCharacteristic) {
        [_peripheral.instructionService.controlInstruction write:isHIDMode click:click doubleClick:doubleClick tripleClick:tripleClick hold:hold clickHold:clickHold handler:handler];
    }
}

- (void)readRSSI:(void (^)(NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    [_peripheral.peripheral readRSSI];
}

- (void)readBattery:(void (^)(NSArray<NSNumber *> * _Nonnull))success
            failure:(void (^)(NSError * _Nullable))failure {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (failure) { failure(ERROR_DISCONNECTED); }
        return;
    }
    [_peripheral.batteryService readBattery:success];
}

- (void)readClickValue:(void (^)(MYNTClickValue, MYNTClickValue, MYNTClickValue, MYNTClickValue, MYNTClickValue))success
               failure:(void (^)(NSError * _Nullable))failure {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (failure) { failure(ERROR_DISCONNECTED); }
        return;
    }
    [_peripheral.hidService readClickValue:success failure:failure];

    if (_peripheral.hidService.isExistCharacteristic) {
        [_peripheral.hidService readClickValue:success failure:failure];
    }
    if (_peripheral.instructionService.isExistCharacteristic) {
        [_peripheral.instructionService.controlInstruction read:^(BOOL isHIDMode,
                                                                  MYNTClickValue click,
                                                                  MYNTClickValue doubleClick,
                                                                  MYNTClickValue tripleClick,
                                                                  MYNTClickValue hold,
                                                                  MYNTClickValue clickHold,
                                                                  NSError * _Nullable error) {
            if (error) {
                if (failure) {
                    failure(error);
                }
                return;
            }
            if (success) {
                success(click, doubleClick, tripleClick, hold, clickHold);
            }
        }];
    }
}

- (void)bindWithPassword:(NSString *)password
                 handler:(void (^ _Nullable)(NSError * _Nullable error))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    [self.peripheral.instructionService.bindInstruction bindWithPassword:password handler:handler];
}

- (void)checkPassword:(NSString *)password
              handler:(void (^ _Nullable)(NSError * _Nullable error))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    [self.peripheral.instructionService.bindInstruction checkPassword:password handler:handler];
}

- (void)writeRingtone:(NSData *)data
              version:(int)version
              handler:(void (^)(NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    [self.peripheral.instructionService.ringtoneInstruction writeRingtone:data version:version handler:handler];
}

- (void)readRingtoneVersion:(void (^)(NSInteger, NSError *))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(0, ERROR_DISCONNECTED); }
        return;
    }
    [self.peripheral.instructionService.ringtoneInstruction readRingtoneVersion:handler];
}

@end

// MARK: - ============================GPS Function============================
@implementation STMynt (MYNT_GPS)

- (void)syncTime:(void (^)(NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    if (self.hardwareType != MYNTHardwareTypeMYNTGPS) {
        if (handler) { handler(ERROR_NOTGPS); }
        return;
    }
    [self.peripheral.instructionService.gpsInstruction syncDate:[NSDate date] handler:handler];
}

- (void)shutdown:(void (^)(NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    if (self.hardwareType != MYNTHardwareTypeMYNTGPS) {
        if (handler) { handler(ERROR_NOTGPS); }
        return;
    }
    [self.peripheral.instructionService.gpsInstruction shutdown:handler];
}

- (void)writeAPN:(NSString *)apn
         handler:(void (^)(NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    if (self.hardwareType != MYNTHardwareTypeMYNTGPS) {
        if (handler) { handler(ERROR_NOTGPS); }
        return;
    }
    [self.peripheral.instructionService.gpsInstruction writeAPN:apn handler:handler];
}

- (void)writeLocateInterval:(NSInteger)minute
                    handler:(void (^)(NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    if (self.hardwareType != MYNTHardwareTypeMYNTGPS) {
        if (handler) { handler(ERROR_NOTGPS); }
        return;
    }
    [self.peripheral.instructionService.gpsInstruction writeLocateInterval:minute handler:handler];
}

- (void)readLocateInterval:(void (^)(NSInteger, NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(0, ERROR_DISCONNECTED); }
        return;
    }
    if (self.hardwareType != MYNTHardwareTypeMYNTGPS) {
        if (handler) { handler(0, ERROR_NOTGPS); }
        return;
    }
    [self.peripheral.instructionService.gpsInstruction readLocateInterval:handler];
}

- (void)readICCID:(void (^)(NSString * _Nullable, NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(nil, ERROR_DISCONNECTED); }
        return;
    }
    if (self.hardwareType != MYNTHardwareTypeMYNTGPS) {
        if (handler) { handler(0, ERROR_NOTGPS); }
        return;
    }
    [self.peripheral.instructionService.gpsInstruction readICCID:handler];
}

- (void)checkNetwork:(void (^)(NSError * _Nullable))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    if (self.hardwareType != MYNTHardwareTypeMYNTGPS) {
        if (handler) { handler(ERROR_NOTGPS); }
        return;
    }
    [self.peripheral.instructionService.checkInstruction checkNetwork:handler];
}

@end

@implementation STMynt (Private)

- (void)setSTPeripheral:(STPeripheral *)peripheral {
    self.peripheral = peripheral;
}

- (STPeripheral *)getSTPeripheral {
    return self.peripheral;
}

- (NSString *)getUUID {
    return self.uuid;
}

- (void)setDiscovering:(BOOL)isDiscovering {
    _isDiscovering = isDiscovering;
}

@end

@implementation STMynt (SlightechPrivate)

// 绑定密码
- (void)sendPassword:(NSString * _Nullable)password
             handler:(void (^ _Nullable)(NSError * _Nullable error))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    [self.peripheral.instructionService.bindInstruction bindWithPassword:password handler:handler];

}

// 校验密码
- (void)checkPassword:(NSString * _Nullable)password
              handler:(void (^ _Nullable)(NSError * _Nullable error))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    [self.peripheral.instructionService.bindInstruction checkPassword:password handler:handler];
}

// 写入运动灵敏度
- (void)writeMotionSensibility:(NSInteger)sensibility
                       handler:(void (^ _Nullable)(NSError * _Nullable error))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    if (self.hardwareType != MYNTHardwareTypeMYNTGPS) {
        if (handler) { handler(ERROR_NOTGPS); }
        return;
    }
    [self.peripheral.instructionService.gpsInstruction writeMotionSensibility:sensibility handler:handler];
}

- (void)writeDBM:(NSInteger)dbm
         handler:(void (^ _Nullable)(NSError * _Nullable error))handler {
    if (_peripheral.logicConnectState != MYNTStateConnected) {
        if (handler) { handler(ERROR_DISCONNECTED); }
        return;
    }
    if (self.hardwareType != MYNTHardwareTypeMYNTGPS) {
        if (handler) { handler(ERROR_NOTGPS); }
        return;
    }
    [self.peripheral.instructionService.gpsInstruction writeDBM:dbm handler:handler];
}

@end

