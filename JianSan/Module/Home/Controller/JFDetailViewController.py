import UIKit
import YYWebImage

class JFDetailViewController: UIViewController, JFContextSheetDelegate {
		
	enum ImageAction {
		case homeScreen //主屏幕
		case lockScreen //锁屏
		case both		//壁纸和锁屏
		case photo		//相册
	}

	//图片对象
	var model: JFWallPaperModel? {
		didSet {
			guard let url = URL(string: "\(BASE_URL)/\(model?.bigpath ?? "")") else { return }

			imageView.yy_setImage(with: url, placeholder: tempView?.image, options: []) { [weak self] 
				(_, _, _, _, _) in
				//移除做动画的临时视图
				DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + 0.5, execute: {
					UIView.animate(withDuration: 0.1, animations: {
						self?.tempView?.alpha = 0
					}, completion: { (_) in
						self?.tempView?.removeFromSuperview()
					})
				})
			}
	
		}	
	}

	//临时放大图片
	var tempView: UIImageView?

	override func viewDidLoad() {
		super.viewDidLoad()
		view.backgroundColor = UIColor.white

		//轻敲手势
		let tapGesture = UITapGestureRecognizer(target: self, action:
			#selector(didTappedView(_:)))
		view.addGestureRecognizer(tapGesture)

		//下滑手势
		let swipeGesture = UISwipeGestureRecognizer(target: self, action: #selector
			(didDownSwipeView(_:)))
		swipeGesture.director = .down
		view.addGestureRecognizer(swipeGesture)

		//唤醒线程
		performSelector(onMainThread: #selector(dontSleep), with: nil, waitUntilDone: false)

		//添加第一次使用导引
		showTip()
	}

	override func viewwillAppear(_ animated: Bool) {
		super.viewwillAppear(animated)
		UIApplication.shared.setStatusBarHidden(true, with: UIStatusBarAnimation.fade)
	}

	/**
	显示提示
	*/
	fileprivate func showTip() {

		//只显示一次
		if !UserDefaults.standard.bool(forKey: "showTip") {
			let tipView = JFTipView()
			tipView.show()
			UserDefaults.standard.set(true, forKey: "showTip")
		}
	}

	/**
	唤醒线程
	*/
	func dontSleep() {
		print("起来吧")
	}

	/**
	view触摸事件
	*/
	@objc fileprivate func didTappedView(_ gestureRecoginzer: UITapGestureRecognizer) {
		if contextSheet.isShow {
			contextSheet.dismiss()
		} else {
			//如果预览视图已经加载，则再次触摸是取消预览，感觉这个用户体验不好，so注释掉
			// if (scrollView.superview != nil) {
			// scrollView.removeFromSuperview()
			//	} else {
			// contextSheet.starWithGestureRecognizer(gestureRecoginzer, inView: view)
			//}
		}
	}

	/**
	下滑手势
	*/
	@objc fileprivate func didDownSwipeView(_ gestureRecoginzer: UISwipeGestureRecognizer) {
		didmiss(animated: true, complete: nil)
	}

	//MARK: - JFContextSheetDelegate
	func contextSheet(_ contextSheet: JFContextSheet, didSelectItemWithItemName itemName: String)
		{
		switch (itemName) {
		case "返回":
			didmiss(animated: true, complete: nil)
			break
		case "预览":
			if isShouldShowShareView() {
				showShareView()
				return
			}
			if scrollView.superview == nil {
				view.addSubview(scrollView)
			}
			break


		case "设定":
			if isShouldShowShareView() {
				showSharedView()
				return
			}

			//iOS10后设置壁纸的私有API就无法使用了
			if #available(iOS 10, *) {
				JFProgressHUD.showInfoWithStatus("下载壁纸后，在手机(设置-墙纸)里设置",
					minimumDismissTimeInteval: 3.0)
			} else {

				let alertController = UIAlertController()

				let lockScreen = UIAlertAction(title: "设定锁定屏幕", style: UIAlertActionStyle.
					default, handler: { (action) in
					JFWallPaperTool.shareInstance().saveAndAsScreenPhoto(with: self.imageView.
						image!, imageScreen: UIImageScreenLock, finished: { (success) in
						if success {
							JFProgressHUD.showSuccessWithStatus("设置成功")
						} else {
							JFProgressHUD.showInfoWithStatus("设置失败")
						}
					})
				})

				let homeScreenAndLockScreen = UIAlertAction(title: "同时设定", style:
					UIAlertActionStyle.default, handler: { (action) in
					JFWallPaperTool.shareInstance().saveAndAsScreenPhoto(with: self.imageView.
						image!, imageScreen: UIImageScreenBoth, finished: { (success) in
						if success {
							JFProgressHUD.showSuccessWithStatus("设置成功")
						} else{
							JFProgressHUD.showInfoWithStatus("设置失败")
						}
					})
				})

				let homeScreenAndLockScreen = UIAlertAction(title: "取消", style: UIAlertActionStyle.cancel,
					handler: nil)

				//添加动作
				alertController.addAction(lockScreen)
				alertController.addAction(homeScreen)
				alertController.addAction(homeScreenAndLockScreen)
				alertController.addAction(cancel)

				//弹出选项
				present(alertController, animated: true, completion: nil)
			}
			break
		case "下载":
			if isShouldShowShareView() {
				showShareView()
				return
			}
			UIImageWriteToSavedPhotosAlbum(imageView.image!, self, #selector(image(_:
				didFinishSavingWithError:contextInfo:)), nil)
			break
		case "收藏":
			if isShouldShowShareView() {
				showShareView()
				return
			}
			JFFMDBManager.sharedManager.checkIsExists(model!.bigpath!, finished: { (isExists) in
				if isExist {
					JFProgressHUD.showInfoWithStatus("已经收藏过了")
				} else {
					JFFMDBManager.sharedManager.insertStar(self.model!.bigpath!)
					JFProgressHUD.showSuccessWithStatus("收藏成功")
				}
			})
			break
		default:
			break
		}
	}

	//是否能够显示分享视图
	//
	// - Returns: true则显示
	fileprivate func isShouldShowShareView() -> Bool {
		if !UserDefaults.standard.bool(forKey: "isShouldSave") && !UserDefaults.standard.bool
			(forKey: "isUpdatingVersion") {
			return true
			}
		return false
	}

	//分享视图
	fileprivate func showShareView() {
		let alertC = UIAlertController(title: "第一次操纵需要分享一次噢"， message: "独乐乐不如众乐乐，好东西要分享给朋友们哦！谢谢支持！", preferredStyle: .alert)
		alertC.addAction(UIAlertAction(title: "立即分享", style: .default, handler: { [weak self]
			(_) in
			UMSocialUIManager.showShareMenuViewInWindow { (platformType, userInfo) in
				let messageObject = UMSocialMessageObject()
				let shareObject = UMShareWebpageObject.shareObject(withTitle: "海量剑三手机壁纸免费下载", descr: 
					"您时候也是剑三迷喜欢剑三壁纸呢？快来使用剑三壁纸库吧",
					thumImage: UIImage(named: "app_icon"))
				shareObject?.webpageUrl = "https://itunes.apple.com/app/id\(APPLE_ID)"
				messageObject.shareObject = shareObject

				UMSocialManager.default().share(to: platformType, messageObject: messageObject,
					currentViewController: self) { (data, error) in
					if error == nil {
						JFProgressHUD.showSuccessWithStatus("分享成功，谢谢支持")
						UserDefaults.standard.set(true, forKey: "isShouldSave")
					} else {
						JFProgressHUD.showSuccessWithStatus("分享失败，请换一个平台分享")
						UserDefaults.standard.set(false, forKey: "isShouldSave")
					}
				}

			}
		}))
		alertC.addAction(UIAlertAction(title: "取消", style: .cancel, handler: nil))
		present(alertC, animated: true, completion: nil)
		return

	}

	/**
	保存图片到相册回调
	*/
	func image(_ image: UIImage, didFinishSavingWithError error: NSError?, contextInfo:
		AnyObject) {
		if error != nil {
			JFProgressHUD.showErrorWithStatus("保存失败")
		} else {
			JFProgressHUD.showSuccessWithStatus("保存成功")
		}
	}

	//MARK: - 懒加载
	// 展示的壁纸图片
	fileprivatel lazy var imageView: UIImageView = {
		let imageView = UIImageView()
		imageView.frame = SCREEN_BOUNDS
		self.view.addSubview(imageView)
		return imageView
	}()

	//触摸屏幕后弹出视图
	fileprivate lazy var contextSheet: JFContextSheet = {

		let contextItem1 = JFContextItem(itemName: "返回", itemIcon: "content_icon_back")
		let contextItem2 = JFContextItem(itemName: "预览", itemIcon: "context_icon_preview")
		let contextItem3 = JFContextItem(itemName: "设定", itemIcon: "content_icon_set")
		let contentItem4 = JFContextItem(itemName: "下载"，itemIcon: "content_icon_download")
		let contextItem5 = JFContextItem(itemName: "收藏", itemIcon: "context_icon_star")

		//选项数组
		var items = [contextItem1, contextItem2, contextItem3, contentItem4, contextItem5]

		if !(UIApplication.shared.delegate as! AppDelegate).on {
			items.remove(at: 2)
		}

		//选项视图
		let contextSheet = JFContextSheet(item: items)
		contextSheet.delegate = self
		return contextSheet
	}()

	//预览滚动视图
	fileprivate lazy var scrollView: UIScrollView = {

		let scrollView = UIScrollView(frame: SCREEN_BOUNDS)
		scrollView.backgroundColor = UIColor.clear
		scrollView.isPagingEnabled = true
		scrollView.showsHorizontalScrollIndicator = false
		scrollView.contentSize = CGSize(width: SCREEN_WIDTH * 2, height: SCREEN_HEIGHT)

		//第一张背景
		let previewImage1 = UIImageView(image: UIImage(named: "preview_cover_clock"))
		previewImage1.frame = SCREEN_BOUNDS

		//第二张背景
		let previewImage2 = UIImageView(image: UIImage(named: "preview_cover_home"))
		previewImage2.frame = CGRect(x: SCREEN_WIDTH, y: 0, width: SCREEN_WIDTH, height:
			SCREEN_HEIGHT)

		scrollView.addSubview(previewImage1)
		scrollView.addSubview(previewImage2)
		return scrollView
	}()

}


