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

    fileprivate let userDefaults = UserDefaults.standard
    fileprivate let settings = SettingsManager.sharedManager

    fileprivate struct About {
        static let weiboURL = "https://weibo.com/2546922913"
        static let homepageURL = "https://jimmylee05.github.io"
        static let appStoreURL =
        "https://itunes.apple.com/us/app/pomodoro-flow/id1095742214?ls=1&mt=8"
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        setupLabels()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)

        if let selectedIndexPath = tableView.indexPathForSelectedRow {
            tableView.deselectRow(at: selectedIndexPath, animated: true)
        }
    }

    // Label显示的内容是随设置的不同而改变的
    fileprivate func setupLabels() {
        pomodoroLengthLabel.text = "\(settings.pomodoroLength / 60) 分钟"
        shortBreakLengthLabel.text = "\(settings.shortBreakLength / 60) 分钟"
        longBreakLengthLabel.text = "\(settings.longBreakLength / 60) 分钟"
        targetPomodorosLabel.text = "\(settings.targetPomodoros) 番茄"
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
                picker.specifier = "pomodoros"
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
