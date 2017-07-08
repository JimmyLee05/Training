#import "InputViewPluginImagePicker.h"
#import <YWExtensionForCustomerServiceFMWK/YWExtensionForCustomerServiceFMWK.h>
#import <WXOpenIMSDKFMWK/YWFMWK.h>
#import <WXOUIModule/YWUIFMWK.h>
#import "MYNT-Swift.h"

@interface InputViewPluginImagePicker()

@property (nonatomic, readonly) YWConversationViewController *conversationViewController;

@end

@implementation InputViewPluginImagePicker

- (YWConversationViewController *)conversationViewController {
	if ([self.inputViewRef.controllerRef isKindOfClass:[YWConversationCViewController class]]) {
		return (YWConversationCViewController *)self.inputViewRef.controllerRef;
	} else {
		return nil
	}
}

#pragma mark - YWInputViewPluginProtocol

- (UIImage *)prepositionPluginNormalIcon {
    UIImage *image = [UIImage imageWithContentsOfFile:[[NSBundle bundleWithPath:[[NSBundle mainBundle] pathForResource:@"CustomerCareResource" ofType:@"bundle"]] pathForResource:@"q_a_photo_btn@2x" ofType:@"png"]];
    return image;
}

// 插件名称
- (NSString *)pluginName {
    return @"选择图片";
}
// 插件对应的view，会被加载到inputView上
/// 你必须提供一个固定的view，而不是每次都重新生成，否则在收拢面板时无法移除该view
- (UIView *)pluginContentView {
    return nil;
}

// 插件被选中运行
/// 你可以在这个里面，调用'YWMessageInputView.h'的'pushContentViewOfPlugin:'函数，控制显示出'pluginContentView'的面板
- (void)pluginDidClicked {
    // 打开选择器
    __weak typeof(self) weakSelf = self;
    [[SelectImageUtils shared] selectImageWithViewController:[self conversationViewController] edit:NO title:@"" selectionItems:@[] selectionHandler:^(NSInteger idx) {

    } imageHandler:^(UIImage * _Nonnull image) {
        YWMessageBodyImage *imageMessageBody = [[YWMessageBodyImage alloc] initWithMessageImage:image];
        [weakSelf.conversationViewController.conversation asyncSendMessageBody:imageMessageBody progress:nil completion:NULL];
    }];
}

- (YWInputViewPluginPosition)pluginPosition {
    return YWInputViewPluginPositionLeft;
}

@end