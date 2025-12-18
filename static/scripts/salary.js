import { calcShiftHours, sumHours, calcShiftMinutes, sumMinutes } from './hour.js';

/**
 * 時給と勤務時間から給与（円）を計算
 * @param {number} hourly - 時給（円）
 * @param {number} hours - 勤務時間（時間）
 * @returns {number} 給与（円、小数第2位丸め）
 */
export function calcSalary(hourly, hours) {
	const value = Number(hourly) * Number(hours);
	return Math.round(value * 100) / 100;
}

/**
 * 単一シフトの給与（円）
 * @param {Object} shift - {start,end,breakStart?,breakEnd?}
 * @param {number} hourly - 時給（円）
 * @returns {number}
 */
export function calcShiftSalary(shift, hourly) {
	const hours = calcShiftHours(shift);
	return calcSalary(hourly, hours);
}

/**
 * 複数シフトの月次合計給与（円）
 * @param {Array<{start:string,end:string,breakStart?:string,breakEnd?:string}>} shifts
 * @param {number} hourly - 時給（円）
 * @returns {number}
 */
export function sumSalary(shifts = [], hourly) {
	const hours = sumHours(shifts);
	return calcSalary(hourly, hours);
}

/**
 * 分単位を使った給与計算（推奨）
 * @param {number} hourly - 時給（円）
 * @param {number} minutes - 勤務時間（分）
 * @returns {number}
 */
export function calcSalaryFromMinutes(hourly, minutes) {
	const value = Number(hourly) * (Number(minutes) / 60);
	return Math.round(value * 100) / 100;
}

/**
 * 単一シフトの給与（分単位）
 * @param {Object} shift - {start,end,breakStart?,breakEnd?}
 * @param {number} hourly - 時給（円）
 * @returns {number}
 */
export function calcShiftSalaryMinutes(shift, hourly) {
	const minutes = calcShiftMinutes(shift);
	return calcSalaryFromMinutes(hourly, minutes);
}

/**
 * 複数シフトの合計給与（分単位）
 * @param {Array<{start:string,end:string,breakStart?:string,breakEnd?:string}>} shifts
 * @param {number} hourly - 時給（円）
 * @returns {number}
 */
export function sumSalaryFromMinutes(shifts = [], hourly) {
	const minutes = sumMinutes(shifts);
	return calcSalaryFromMinutes(hourly, minutes);
}

// 使い方例:
// const shifts = [
//   { start: '09:00', end: '17:30', breakStart: '12:30', breakEnd: '13:30' },
//   { start: '22:00', end: '06:00' } // 深夜跨ぎ
// ];
// const hourly = 1200; // 円
// console.log('hours=', sumHours(shifts));
// console.log('salary=', sumSalary(shifts, hourly));

