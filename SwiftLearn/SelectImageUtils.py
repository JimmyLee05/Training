import UIKit
import MYNTKit

class SelectImageUtils: NSObject, UIActionSheetDelegate, UINavigationControllerDelegate,
	UIImagePickerControllerDelegate {

	static let shared = SelectImageUtils()

	private var _imageHandler: ((UIImage) -> Void)?
	private weak var _viewController: UIViewController?
	private var _edit = true
	private var _selectionHandler: ((Int) -> Void)?

	private override init() {
		super.init()
	}

	func selectImageFromPhotos(viewController: UIViewController,
							   edit: Bool = false,
							   imageHandler: @escaping (UIImage) -> Void)) {
		_viewController = viewController
		_edit = edit
		_imageHandler = imageHandler
		self.localPhoto()		
	}

	func selectImageFromCamera(viewController: UIViewController,
							   edit: Bool = false,
							   imageHandler: @escaping ((UIImage) -> Void)) {
		_viewController = viewController
		_edit = edit
		_imageHandler = imageHandler
		self.takePhoto()
	}

	func selectImage(viewController: UIViewController,
					 edit: Bool,
					 title: String = "选择一张照片",
					 selectionItems: [String]? = nil,
					 selectionHandler: ((Int) -> Void)? = nil,
					 imageHandler: @escaping ((UIImage) -> Void)) {
		_viewController = viewController
		_imageHandler = imageHandler
		_selectionHandler = selectionHandler
		_edit = edit

		let actionSheet = UIActionSheet(title: title,
										delegate: self,
										cancelButtonTitle: NSLocalizedString("CANCEL", comment: "取消"),
										destructiveButtonTitle: nil)
		actionSheet.addButton(withTitle: NSLocalizedString("CAMERA", comment: "拍照"))
		actionSheet.addButton(withTitle: NSLocalizedString("GALLERY", comment: "相册"))

		if selectionItems != nil {
			for title in selectionItems! {
				actionSheet.addButton(withTitle: title)
			}
		}
		actionSheet.show(in: UIApplication.shared.keyWindow!)
	}

	func actionSheet(_ actionSheet: UIActionSheet, clickedButtonAt buttonIndex: Int) {
		if buttonIndex == actionSheet.cancelButtonIndex {
			return 
		}
		switch buttonIndex {
		case 1:
			self.takePhoto()
		case 2:
			self.localPhoto()
		default:
			_selectionHandler?(buttonIndex - 3)
		}
	}

	func takePhoto() {
		let sourceType = UIImagePickerControllerSourceType.camera
		let status = AVCaptureDevice.authorizationStatus(forMediaType: AVMediaTypeVideo)
		if status == .denied || status == .restricted {
			DislogManage.shared.show()
		}
	}



















