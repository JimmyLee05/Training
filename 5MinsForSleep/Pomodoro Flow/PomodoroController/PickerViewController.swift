//
//  PickerViewController.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/15.
//  Copyright © 2018年 JimmyLee. All rights reserved.
//

import UIKit

protocol PickerViewControllerDelegate: class {
    func pickerDidFinishPicking(_ picker: PickerViewController)
}

class PickerViewController: UITableViewController {

    var options: [Int]!
    var specifier = "分钟"

    var type: PickerType!
    var selectedValue: Int!
    var selectedIndexPath: IndexPath?
    var delegate: PickerViewControllerDelegate?

    fileprivate struct PickerOptions {
        static let pomodoroLength = [1, 2, 3, 4, 5].map { $0 * 60 }
        static let shortBreakLength = [1, 2, 3, 4, 5].map { $0 * 60 }
        static let longBreakLength = [1].map { $0 * 60 }
        static let targetPomodoros = [7].map { $0 }
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        switch type! {
        case .pomodoroLength: options = PickerOptions.pomodoroLength
        case .shortBreakLength: options = PickerOptions.shortBreakLength
        case .longBreakLength: options = PickerOptions.longBreakLength
        case .targetPomodoros: options = PickerOptions.targetPomodoros
        }
        if let index = options.index(of: selectedValue), type != .targetPomodoros {
            selectedIndexPath = IndexPath(row: index, section: 0)
        }
    }

    // MARK: - Table view data source
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return options.count
    }

    override func tableView(_ tableView: UITableView,
                            cellForRowAt indexPath: IndexPath) -> UITableViewCell {

        let cell = tableView.dequeueReusableCell(withIdentifier: "PickerCell",
                                                 for: indexPath)
        // 配置cell
        let value = options[indexPath.row]
        let formattedValue = (type == PickerType.targetPomodoros ? value : value / 60)
        cell.textLabel?.text = "\(formattedValue) \(specifier)"

        let currentValue = options[indexPath.row]

        if currentValue == selectedValue {
            cell.accessoryType = .checkmark
            selectedIndexPath = indexPath
        } else {
            cell.accessoryType = .none
        }
        return cell
    }

    override func tableView(_ tableView: UITableView,
                            didSelectRowAt indexPath: IndexPath) {

        tableView.deselectRow(at: indexPath, animated: true)

        // 如果选择的新值和之前的值一样，则返回
        if options[indexPath.row] == selectedValue {
            return
        }

        // 标记新的选项
        if let newCell = tableView.cellForRow(at: indexPath) {
            newCell.accessoryType = .checkmark
        }

        // 标记新的选项后，将标记从之前的选项移除
        if let previousIndexPath = selectedIndexPath,
            let oldCell = tableView.cellForRow(at: previousIndexPath) {
            oldCell.accessoryType = .none
        }

        selectedIndexPath = indexPath
        selectedValue = options[indexPath.row]
        updateSettings()
    }

    // Navigating back
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)

        if isMovingFromParentViewController {
            delegate?.pickerDidFinishPicking(self)
        }
    }
    // 更新设置选项
    fileprivate func updateSettings() {
        let settings = SettingsManager.shared

        switch type! {
        case .pomodoroLength:
            settings.pomodoroLength = selectedValue
        case .shortBreakLength:
            settings.shortBreakLength = selectedValue
        case .longBreakLength:
            settings.longBreakLength = selectedValue
        case .targetPomodoros:
            settings.targetPomodoros = selectedValue
        }
    }
}
