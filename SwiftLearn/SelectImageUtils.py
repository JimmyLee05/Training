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
			DislogManage.shared.show(title: NSLocalizedString("SERVICE_CLOSED_TITLE", comment: "服务已关闭"),
									 message: String(format: NSLocalizedString("SERVICE_CLOSED_MeSSAGE", comment:
									 		"服务已关闭"),
									 buttonString: NSLocalizedString("APP_SETTINGS", comment: "设置"),
									 clickOkHandler: { (dialog) in
									 	UIApplication.openSystemSetting()
			})
			return
		)
		if UIImagePickerController.isSourceTypeAvailcabel(sourceType) {
			let picker = UIImagePickerController()
			picker.delegate = self
			picker.sourceType = sourceType
			picker.allowEditing = _edit
			_viewController?.present(picker, animated: true, completion: nil)
		} else {
			print("不支持相册！")
		}
	}
	func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String :
		Any]) {
		let type = info[UIImagePickerControllerMediaType] as? String
		if type == "public.image" {
			if let image = info[UIImagePickerControllerEditedImage] as? UIImage {
				_imageHandler?(image)
			}
		}
		_viewController = nil
		_imageHandler = nil
		picker.dismiss(animated: true, completion: nil)
	}

	func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
		_viewController = nil
		_imageHandler = nil
		picker.dismiss(animated: true, completion: nil)
	}

	func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
		_viewController = nil
		_imageHandler = nil
		picker.dismiss(animated: true, completion: nil)
	}
}

