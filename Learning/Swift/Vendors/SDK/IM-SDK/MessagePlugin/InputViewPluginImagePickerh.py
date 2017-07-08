#import <Foundation/Foundation.h>
#import <WXOUIModule/YWUIFMWK.h>
#import <WXOpenIMSDKFMWK/YWFMWK.h>

@interface InputViewPluginImagePicker : NSObject<YWInputViewPluginProtocol>

@property (nonatomic, weak) YMMessageInputView *inputViewRef;

@end