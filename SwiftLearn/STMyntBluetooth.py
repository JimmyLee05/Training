#import <Foundation/Foundation.h>
#import "STMynt.h"

@interface STMyntBluetooth: NSObject

@property (nonatomic, assign, readonly) BOOL isScanning;

@property (nonatomic, assign, readonly) CBCentralManagerState centralState;

@property (nonatomic, assign) BOOL isReportUnknownMynt;

@property (nonatomic, weak, nullable) id<STMyntBluetoothDelegate> delegate;

+ (instancetype _Nonnull)sharedInstance;

- (void)setMyntAppKey:(NSString * _Nonnull)appKey;

- (void)setCustomParams:(NSString * _Nullable)params;

- (void)startScan;

- (void)stopScan;

- (STMynt * Nullable)findMyntWithSn: (NSString *_Nonnull)sn;

@end