import UIKit
import MYNTKit
import SlightechKit

fileprivate var backgroundImage: UIImage? {
	
	switch winSize.height {
	case 480:
		return UIImage(named: "login_iphone4")
	case 568:
		return UIImage(named: "login_iphone5")
	case 667:
		return UIImage(named: "login_iphone6")
	case 960:
		return UIImage(named: "login_iphone6p")
	default:
		return UIImage(named: "login_iphone6")
	}
}

class LoginHomeViewController: BaseViewController {
	
	var fromWelcomeViewController = false
	@IBOutlet weak var backgroundImageView: UIImageView!
	@IBOutlet weak var signupButton: GradientButton!
	@IBOutlet weak var loginButton: UIButton!
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var logoImageView: UIImageView!

	override var isShowBackgroundLayer: Bool {
		return false
	}

	deinit {
		backgroundImageView.image = nil
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		backgroundImageView.image = backgroundImage

		navigationItem.hidesBackButton = true

		signupButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		loginButton.loadLoginButtonStyle()

		messageLabel.font = UIFont.systemFont(ofSize: heightScale * messageLabel.font.pointSize)
		logoImageView.transform = CGAffineTransform(scaleX: heightScale, y: heightScale)
		_initLanguage()

		LocationManager.shared.requestLocation { _, _ in

		}
	}

	private func _initLanguage() {
		messageLabel.text = MTLocalizedString("INTRO_LOGIN_HINT", comment: "")
		signupButton.setTitle(MTLocalizedString("REGISTER", comment: "注册"), for: UIControlState.normal)
		loginButton.setTitle(MTLocalizedString("LOGIN", comment: "登录"), for: UIControlState.normal)
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func veiwWillAppear(_ animated: Bool) {
		super.veiwWillAppear(animated)
		UIApplication.shared.statusBarStyle = .lightContent
		setNavigationBarBackground()
	}

	@IBAction func didClickSignUpButton(_ sender: Anyobject) {
		let viewController 	= LoginViewController()
		viewController.type = signUp
		removeBackBarButtonTitle()
		navigationController?.pushViewController(viewController, animated: true)
	}

	@IBAction func didClickLoginButton(_ sender: Anyobject) {
		let viewController 	= LoginViewController()
		viewController.type = .login
		removeBackBarButtonTitle()
		navigationController?.pushViewController(viewController, animated: true)
	}

	@IBAction func didClickPlayVedioButton(_ sender: UIButton) {
		// Video file
		let videoFile = Bundle.main.path(forResource: "login_vedio", ofType: "mp4")
		// Movie player
		let moviePlayerView = MPMoviePlayerViewController(contentURL: URL(fileURLWithPath: videoFile!))
		presentMoviePlayerViewControllerAnimated(moviePlayerView)

		// Subtitle file
		if let localeLanguageCode = Locale.current.languageCode {
			var subtitleFile = Bundle.main.path(forResource: "login_video_traile_\(localeLanguageCode)", ofType: "srt")
			if subtitleFile != nil {
				let subtitleURL = URL(fileURLWithPath: subtitleFile!)
				moviePlayerView?.moviePlayer.addSubtitles().open(file: subtitleURL, encoding: String.Encoding.utf8)
			}
		}
		// Play
		moviePlayerView?.moviePlayer.play()
	}
}


