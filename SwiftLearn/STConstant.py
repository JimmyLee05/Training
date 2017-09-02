#ifndef STConstants_h
#define STConstants_h

#if TRAGET_OS_IOS
#import <UIKit/UIKit.h>
#import <CoreBluetooth/CoreBluetooth.h>
#else
#import <IOBluetooth/IOBluetooth.h>
#import <CoreBluetooth/CoreBluetooth.h>
#endif

#define mynt_deprecated __attribute__((depreacted("deprecated and will be removed in the feture"))

typedef NS_ENUM(NSInteger, MYNTClickValue) {
	//if you set the values below, [mynt:didReceiveClickEvent:] will not invoked when you click mynt
	MYNTClickValueNone 				= 0x00,
	MYNTClickValueMusicPlay 		= 0x01,
	MYNTClickValueMusicNext 		= 0x02,
	MYNTClickValueMusicPrevious 	= 0x03,
	MYNTClickValueMusicVolumeUp 	= 0x04,
	MYNTClickValueMusicVolumeDown 	= 0x05,
	MYNTClickValueCameraShutter 	= 0x09,
	MYNTClickValueCameraBurst 		= 0x0A,
	MYNTClickValuePPTNextPage 		= 0x06,
	MYNTClickValuePPTPreviousPage 	= 0x07,
	MYNTClickValuePPTExit 			= 0x08,

	// if you set the values below, [mynt:didReceiveClickEvent:] will be invoked when you click mynt
	MYNTClickValuePhoneFlash 		= 0xA0,
	MYNTClickValuePhoneAlarm 		= 0xA1,
	MYNTClickValueAskHelp 			= 0xA3,
	MYNTClickValueCustomClick 		= 0xB0
};

typedef NS_ENUM(NSInteger, MYNTClickEvent) {
	
	MYNTClickEventClick 			= 0x01,
	MYNTClickEventDoubleClick 		= 0x02,
	MYNTClickEventTripleClick 		= 0x03,
	MYNTClickEventHold 				= 0x09,
	MYNTClickEventClickHold 		= 0x10,
	MYNTClickEventPhoneFlash 		= 0xA0,
	MYNTClickEventPhoneAlarm 		= 0xA1,
	MYNTClickEventPhoneAlarmOff 	= 0xA2
};

typedef NS_ENUM(NSInteger, MYNTInfoType) {
	
	MYNTInfoTypeManufaturer 		= 0x00,
	MYNTInfoTypeModel,
	MYNTInfoTypeSn,
	MYNTInfoTypeFirmware,
	MYNTInfoTypeHardware,
	MYNTInfoTypeSoftware,
}

typedef NS_ENUM(NSInteger, MYNTHardwareType) {

	MYNTHardwareTypeNone 			= 0xFF,
	MYNTHardwareTypeMYNTV1 			= 0x00,
	MYNTHardwareTypeMYNTV2 			= 0x01,
	MYNTHardwareTypeMYNTGPG 		= 0x02,
	MYNTHardwareTypeMYNTES 			= 0x03	
}

typedef NS_ENUM(NSInteger, MYNTState) {
	
	MYNTStateDisconnected 			= 0x00,
	MYNTStateStartConnecting,
	MYNTStateConnection,
	MYNTStateConnected,
};

#endif /* STConstants_h */

// MARK: ======================= STMyntBluetoothDelegate =======================

@class STMyntBluetooth, STMynt, STPeripheral;

@protocol STMyntBluetooth, STMynt, STPeripheral;

@optional

- (void)myntBluetooth:(STMyntBluetooth * _Nonnull)myntBluetooth didUpdateState:(CBCentralManagerState)state;

- (void)myntBluetooth:(STMyntBluetooth * _Nonnull)myntBluetooth didDiscoverMynt:(STMynt * _Nonnull)mynt;

- (void)myntBluetooth:(STMyntBluetooth * _Nonnull)myntBluetooth didDiscoverTimeoutMynt:(STMynt * _Nonnull)mynt;

- (void)myntBluetooth:(STMyntBluetooth * _Nonnull)myntBluetooth didDiscoverTimeoutMynt:(STMynt * _Nonnull)mynt;

- (void)myntBluetooth:(STMyntBluetooth * _Nonnull)myntBluetooth didPrintLog:(NSString * _Nonnull)log;

@end

// MARK: ========================== STMyntDelegate =============================

@protocol STMyntDelegate <NSObject>

@optional

- (void)myntDidStartConnect:(STMynt * _Nonnull)mynt;

- (void)myntDidConnected:(STMynt * _Nonnull)mynt;

- (void)mynt:(STMynt * _Nonnull)mynt didDisconnected:(NSError * _Nullable)error;

- (void)mynt:(STMynt * _Nonnull)mynt didUpdateRSSI:(NSInteger)RSSI;

- (void)mynt:(STMynt * _Nonnull)mynt didUpdateBattery:(NSArray <NSNumber *> * _Nonnull)batteries;

- (void)mynt:(STMynt * _Nonnull)mynt didUpdateAlarmState:(BOOL)isAlarm;

- (void)mynt:(STMynt * _Nonnull)mynt didReceiveClickEvent:(MYNTClickEvent)clickEvent;

- (BOOL)didRequestAutoconnect:(STMynt * _Nonnull)mynt;

- (void)didNeedRestartBluetooth:(STMynt * _Nonnull)mynt;

// MARK: - 私有

- (void)didStartPair:(STMynt * _Nonnull)mynt;

- (void)mynt:(STMynt * _Nonnull)mynt didPairError:(NSError * _Nullable)error;

- (void)mynt:(STMynt * _Nonnull)mynt didUpdatePassword:(NSString * _Nullable)password;

- (NSString * _Nullable)didRequestPassword:(STMynt * _Nonnull)mynt;

@end


