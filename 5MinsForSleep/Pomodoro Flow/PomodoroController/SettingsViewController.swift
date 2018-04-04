//
//  SettingsViewController.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/15.
//  Copyright © 2018年 JimmyLee. All rights reserved.
//

import UIKit

// Setting界面的设置
class SettingsViewController: UITableViewController, PickerViewControllerDelegate {

    @IBOutlet weak var pomodoroLengthLabel: UILabel!
    @IBOutlet weak var shortBreakLengthLabel: UILabel!
    @IBOutlet weak var longBreakLengthLabel: UILabel!
    @IBOutlet weak var targetPomodorosLabel: UILabel!

    // About section
    @IBOutlet weak var twitterCell: UITableViewCell!
    @IBOutlet weak var homepageCell: UITableViewCell!
    @IBOutlet weak var appStoreCell: UITableViewCell!

    @IBOutlet weak var timeImageView: UIImageView!
    @IBOutlet weak var shortImageView: UIImageView!
    @IBOutlet weak var longImageView: UIImageView!
    @IBOutlet weak var targetImageView: UIImageView!
    

    @IBOutlet weak var weiboImageView: UIImageView!
    @IBOutlet weak var blogImageView: UIImageView!
    @IBOutlet weak var storeImageView: UIImageView!
    @IBOutlet weak var versionImageView: UIImageView!

    let timeImage       = UIImage(named: "time")
    let shortImage      = UIImage(named: "shortsleep")
    let longImage       = UIImage(named: "longsleep")
    let targetImage     = UIImage(named: "target")
    let weiboImage      = UIImage(named: "weibo")
    let blogImage       = UIImage(named: "blog")
    let storeImage      = UIImage(named: "app store")
    let versionImage    = UIImage(named: "version")

    fileprivate let userDefaults = UserDefaults.standard
    fileprivate let settings = SettingsManager.shared

    fileprivate struct About {
        static let weiboURL     = "https://www.bilibili.com/video/av13331099?from=search&seid=12552099960711528245"
        static let homepageURL  = "https://jimmylee05.github.io"
        static let appStoreURL  = "https://itunes.apple.com/us/app/pomodoro-flow/id1095742214?ls=1&mt=8"
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        resetImage()
        setupLabels()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)

        if let selectedIndexPath = tableView.indexPathForSelectedRow {
            tableView.deselectRow(at: selectedIndexPath, animated: true)
        }
    }

    fileprivate func resetImage() {
        let reSize = CGSize(width: 30, height: 30)
        timeImageView.image     = timeImage?.reSizeImage(reSize: reSize)
        shortImageView.image    = shortImage?.reSizeImage(reSize: reSize)
        longImageView.image     = longImage?.reSizeImage(reSize: reSize)
        targetImageView.image   = targetImage?.reSizeImage(reSize: reSize)
        weiboImageView.image    = weiboImage?.reSizeImage(reSize: reSize)
        blogImageView.image     = blogImage?.reSizeImage(reSize: reSize)
        storeImageView.image    = storeImage?.reSizeImage(reSize: reSize)
        versionImageView.image  = versionImage?.reSizeImage(reSize: reSize)
    }

    // Label显示的内容是随设置的不同而改变的
    fileprivate func setupLabels() {
        pomodoroLengthLabel.text = "\(settings.pomodoroLength / 60) 分钟"
        shortBreakLengthLabel.text = "\(settings.shortBreakLength / 60) 分钟"
        longBreakLengthLabel.text = "\(settings.longBreakLength / 60) 分钟"
        targetPomodorosLabel.text = "\(settings.targetPomodoros) 个"
    }

    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if let picker = segue.destination as? PickerViewController {
            switch segue.identifier! {
            case "PomodoroLengthPicker":
                picker.selectedValue = settings.pomodoroLength
                picker.type = PickerType.pomodoroLength
            case "ShortBreakLengthPicker":
                picker.selectedValue = settings.shortBreakLength
                picker.type = PickerType.shortBreakLength
            case "LongBreakLengthPicker":
                picker.selectedValue = settings.longBreakLength
                picker.type = PickerType.longBreakLength
            case "TargetPomodorosPicker":
                picker.specifier = "个"
                picker.selectedValue = settings.targetPomodoros
                picker.type = PickerType.targetPomodoros
            default:
                break
            }
            picker.delegate = self
        }
    }

    func pickerDidFinishPicking(_ picker: PickerViewController) {
        setupLabels()
    }

    // MARK: - Table view delegate
    override func tableView(_ tableView: UITableView,
                            didSelectRowAt indexPath: IndexPath) {

        tableView.deselectRow(at: indexPath, animated: true)

        let cell = tableView.cellForRow(at: indexPath)!
        switch cell {
        case twitterCell: openURL(About.weiboURL)
        case homepageCell: openURL(About.homepageURL)
        case appStoreCell: openURL(About.appStoreURL)
        default: return
        }
    }

    // MARK: - Helpers

    fileprivate func openURL(_ url: String) {
        let application = UIApplication.shared

        if let url = URL(string: url) {
            application.openURL(url)
        }
    }

}

extension UIImage {
    /**
     *  重设图片大小
     */
    func reSizeImage(reSize:CGSize)->UIImage {
        //UIGraphicsBeginImageContext(reSize);
        UIGraphicsBeginImageContextWithOptions(reSize,false,UIScreen.main.scale)
        self.draw(in: CGRect(x:0, y:0, width: reSize.width, height: reSize.height))
        let reSizeImage:UIImage = UIGraphicsGetImageFromCurrentImageContext()!
        UIGraphicsEndImageContext()
        return reSizeImage
    }

    /**
     *  等比率缩放
     */
    func scaleImage(scaleSize:CGFloat)->UIImage {
        let reSize = CGSize(width: self.size.width * scaleSize, height: self.size.height * scaleSize)
        return reSizeImage(reSize: reSize)
    }
}
