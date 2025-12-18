/**
 * 時刻文字列をDateに変換（基準日を指定）
 * @param {string} hhmm - "HH:MM" 形式
 * @param {Date} baseDate - 基準日（同日計算のため）
 * @returns {Date}
 */
function toDate(hhmm, baseDate = new Date(2000, 0, 1)) {
	if (!hhmm) return null;
	const [h, m] = hhmm.split(':').map(Number);
	const d = new Date(baseDate.getTime());
	d.setHours(h, m, 0, 0);
	return d;
}

/**
 * 単一シフトの勤務時間（時間）を計算
 * 深夜跨ぎ（終了が開始より早い）や休憩時間を考慮
 * @param {Object} opt
 * @param {string} opt.start - 開始時刻 "HH:MM"
 * @param {string} opt.end - 終了時刻 "HH:MM"
 * @param {string} [opt.breakStart] - 休憩開始 "HH:MM"
 * @param {string} [opt.breakEnd] - 休憩終了 "HH:MM"
 * @returns {number} 勤務時間（小数、時間）
 */
// 分単位で計算（推奨）
export function calcShiftMinutes({ start, end, breakStart, breakEnd }) {
	const base = new Date(2000, 0, 1);
	const s = toDate(start, base);
	const e = toDate(end, base);
	if (!s || !e) return 0;

	// 終了が開始より早い場合は翌日扱い
	let endDt = new Date(e.getTime());
	if (endDt < s) endDt.setDate(endDt.getDate() + 1);

	let workMs = endDt - s; // 総勤務時間（ミリ秒）

	let breakMs = 0;
	if (breakStart && breakEnd) {
		const bs = toDate(breakStart, base);
		const be = toDate(breakEnd, base);
		if (bs && be) {
			let beDt = new Date(be.getTime());
			if (beDt < bs) beDt.setDate(beDt.getDate() + 1);
			breakMs = Math.max(0, beDt - bs);
		}
	}

	const netMs = Math.max(0, workMs - breakMs);
	const minutes = Math.round(netMs / (1000 * 60));
	return minutes; // 分単位（整数）
}

// 従来の時間(小数)計算：分から換算（分精度）
export function calcShiftHours({ start, end, breakStart, breakEnd }) {
	const minutes = calcShiftMinutes({ start, end, breakStart, breakEnd });
	// 分精度を保ったまま時間へ換算（小数第2位に丸め）
	return Math.round((minutes / 60) * 100) / 100;
}

/**
 * 複数シフトの合計勤務時間（時間）
 * @param {Array<{start:string,end:string,breakStart?:string,breakEnd?:string}>} shifts
 * @returns {number}
 */
export function sumMinutes(shifts = []) {
	return shifts.reduce((acc, s) => acc + calcShiftMinutes(s), 0);
}

export function sumHours(shifts = []) {
	const minutes = sumMinutes(shifts);
	return Math.round((minutes / 60) * 100) / 100;
}

