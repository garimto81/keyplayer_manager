function updateAndCheckBoxes() {
  // --- 고유 아이디 설정 ---
  const SOURCE_SPREADSHEET_ID = "1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg"; // Key Player 마스터 리스트 ('Confirmed' 시트)
  const TARGET_SPREADSHEET_ID = "19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4"; // WSOP CSV 데이터 + Key Player 마킹 ('type' 시트)

  Logger.log("🚀 스크립트 실행 시작");

  try {
    // --- 단계 1: SOURCE에서 Key Player 마스터 리스트 로드 ---
    Logger.log(`➡️ [단계 1/3] SOURCE 스프레드시트 (ID: ${SOURCE_SPREADSHEET_ID}) 열기...`);
    const sourceSpreadsheet = SpreadsheetApp.openById(SOURCE_SPREADSHEET_ID);
    const confirmedSheet = sourceSpreadsheet.getSheetByName('Confirmed');
    if (!confirmedSheet) {
      Logger.log("❌ 오류: SOURCE 시트에서 'Confirmed' 탭을 찾을 수 없습니다.");
      return;
    }

    const sourceRange = confirmedSheet.getRange("E2:E" + confirmedSheet.getLastRow());
    const sourceData = sourceRange.getValues();
    const keyPlayersSet = new Set();

    Logger.log(`➡️ [단계 2/3] 'Confirmed' 시트 E열에서 Key Player 마스터 리스트 생성 중...`);
    for (let i = 0; i < sourceData.length; i++) {
      const playerName = sourceData[i][0];
      if (playerName) {
        keyPlayersSet.add(playerName.trim());
      }
    }
    Logger.log(`✅ Key Player 마스터 리스트: 총 ${keyPlayersSet.size}명 로드 완료`);

    // --- 단계 2: TARGET 스프레드시트 업데이트 (CSV 데이터 + Key Player 마킹) ---
    Logger.log(`➡️ [단계 3/3] TARGET 스프레드시트 (ID: ${TARGET_SPREADSHEET_ID})에서 데이터 읽기...`);
    const targetSpreadsheet = SpreadsheetApp.openById(TARGET_SPREADSHEET_ID);
    const typeSheet = targetSpreadsheet.getSheetByName('Type');  // 대문자 T
    if (!typeSheet) {
      Logger.log("❌ 오류: 목표 시트에서 'Type' 탭을 찾을 수 없습니다.");
      return;
    }
    const typeRange = typeSheet.getRange(1, 1, typeSheet.getLastRow(), 12);
    const typeValues = typeRange.getValues();
    Logger.log(`✅ 'type' 시트에서 총 ${typeValues.length} 행의 데이터를 읽었습니다.`);

    // Key Players를 배열로 변환 (부분 일치 매칭용)
    const keyPlayersArray = Array.from(keyPlayersSet);
    Logger.log(`➡️ 'type' 시트 H열(PlayerName)과 Key Player 마스터 리스트 매칭 중...`);

    let matchCount = 0;
    const newValuesForKL = typeValues.map((row, index) => {
      if (index === 0) return [row[10], row[11]]; // 헤더

      const fullName = row[7] ? row[7].trim() : "";
      let kValue = '', lValue = '';

      // 부분 일치 매칭: Confirmed E열 이름이 type H열 이름에 포함되어 있으면 Key Player
      if (fullName) {
        const isKeyPlayer = keyPlayersArray.some(keyName =>
          fullName.toLowerCase().includes(keyName.toLowerCase())
        );

        if (isKeyPlayer) {
          kValue = 'TRUE';
          matchCount++;
        }
      }

      // 이름 축약 로직
      if (fullName) {
        if (fullName.length <= 10) {
          lValue = fullName;
        } else {
          const parts = fullName.split(' ');
          const firstName = parts[0];
          const lastName = parts[parts.length - 1];
          if (parts.length === 1) {
            lValue = fullName;
          } else if (firstName.length <= 2 && firstName.endsWith('.')) {
            lValue = `${firstName} ${lastName}`;
          } else {
            lValue = `${firstName.charAt(0)}. ${lastName}`;
          }
        }
      }
      return [kValue, lValue];
    });

    typeSheet.getRange(1, 11, newValuesForKL.length, 2).setValues(newValuesForKL);
    Logger.log(`✅ 'type' 시트 K열(Key Player), L열(짧은이름) 업데이트 완료!`);
    Logger.log(`   → 총 ${matchCount}명의 Key Player 마킹 완료`);

    Logger.log("🎉 모든 작업이 성공적으로 완료되었습니다.");

  } catch (e) {
    Logger.log(`❌ 예상치 못한 오류 발생: ${e.message}\n오류 위치: ${e.stack}`);
    SpreadsheetApp.getUi().alert(`오류가 발생했습니다: ${e.message}`);
  }
}


/**
 * =============================================================================
 * 자동 실행 기능 (Time-based Trigger)
 * =============================================================================
 */

/**
 * Time Trigger 설정 함수
 * - 1분마다 autoRunIfUpdated() 실행
 * - 실행 방법: Apps Script 편집기에서 이 함수를 1회 수동 실행
 */
function setupTimeTrigger() {
  // 기존 트리거 삭제 (중복 방지)
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'autoRunIfUpdated') {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // 1분마다 실행되는 트리거 생성
  ScriptApp.newTrigger("autoRunIfUpdated")
    .timeBased()
    .everyMinutes(1)
    .create();

  Logger.log("✅ Time Trigger 설정 완료!");
  Logger.log("   → autoRunIfUpdated() 함수가 1분마다 자동 실행됩니다.");
  Logger.log("   → Type 시트 업데이트 감지 시 updateAndCheckBoxes() 자동 실행");

  return "✅ Time Trigger 설정 완료! autoRunIfUpdated()가 1분마다 실행됩니다.";
}


/**
 * 자동 실행 함수 (Time Trigger가 호출)
 * - Type 시트의 마지막 업데이트 시간 확인
 * - 새 데이터가 업로드되면 updateAndCheckBoxes() 실행
 */
function autoRunIfUpdated() {
  try {
    const targetSpreadsheet = SpreadsheetApp.openById(TARGET_SPREADSHEET_ID);
    const typeSheet = targetSpreadsheet.getSheetByName('Type');

    if (!typeSheet) {
      Logger.log("⚠️ Type 시트를 찾을 수 없습니다.");
      return;
    }

    // 현재 시트의 마지막 행 수
    const currentLastRow = typeSheet.getLastRow();

    // Script Properties에서 마지막 처리된 상태 가져오기
    const props = PropertiesService.getScriptProperties();
    const lastProcessedRow = props.getProperty('lastProcessedRow');
    const lastProcessedTime = props.getProperty('lastProcessedTime');

    // A1 셀 값 확인 (헤더 또는 데이터 시작)
    const a1Value = typeSheet.getRange('A1').getValue();
    const lastA1Value = props.getProperty('lastA1Value');

    // 변경 감지: 행 수 변경 또는 A1 값 변경
    const hasChanged = (
      currentLastRow != lastProcessedRow ||
      a1Value != lastA1Value
    );

    if (hasChanged && currentLastRow > 1) {
      Logger.log("🔄 Type 시트 변경 감지!");
      Logger.log(`   이전 행 수: ${lastProcessedRow} → 현재 행 수: ${currentLastRow}`);
      Logger.log(`   A1 값: ${lastA1Value} → ${a1Value}`);

      // Key Player 업데이트 실행
      Logger.log("🚀 updateAndCheckBoxes() 자동 실행 시작...");
      updateAndCheckBoxes();

      // 처리 완료 상태 저장
      props.setProperty('lastProcessedRow', currentLastRow.toString());
      props.setProperty('lastProcessedTime', new Date().toISOString());
      props.setProperty('lastA1Value', a1Value.toString());

      Logger.log("✅ 자동 실행 완료!");
      Logger.log(`   처리 시간: ${new Date().toISOString()}`);
      Logger.log(`   처리된 행 수: ${currentLastRow}`);

    } else if (currentLastRow <= 1) {
      Logger.log("ℹ️ Type 시트가 비어있습니다 (헤더만 존재).");
    } else {
      Logger.log("ℹ️ Type 시트 변경 없음. 대기 중...");
    }

  } catch (e) {
    Logger.log(`❌ 자동 실행 오류: ${e.message}`);
    Logger.log(`   오류 위치: ${e.stack}`);
  }
}


/**
 * Trigger 삭제 함수
 * - 자동 실행을 중단하고 싶을 때 사용
 */
function deleteTimeTrigger() {
  const triggers = ScriptApp.getProjectTriggers();
  let deletedCount = 0;

  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'autoRunIfUpdated') {
      ScriptApp.deleteTrigger(trigger);
      deletedCount++;
    }
  });

  // Script Properties 초기화
  const props = PropertiesService.getScriptProperties();
  props.deleteProperty('lastProcessedRow');
  props.deleteProperty('lastProcessedTime');
  props.deleteProperty('lastA1Value');

  Logger.log(`✅ Time Trigger 삭제 완료 (${deletedCount}개)`);

  return `✅ Time Trigger 삭제 완료 (${deletedCount}개)`;
}


/**
 * Trigger 상태 확인 함수
 * - 현재 설정된 트리거 목록 확인
 */
function checkTriggerStatus() {
  const triggers = ScriptApp.getProjectTriggers();
  const autoTriggers = triggers.filter(t => t.getHandlerFunction() === 'autoRunIfUpdated');

  Logger.log("=".repeat(60));
  Logger.log("📊 Trigger 상태 확인");
  Logger.log("=".repeat(60));

  if (autoTriggers.length > 0) {
    Logger.log(`✅ 자동 실행 활성화됨 (${autoTriggers.length}개 트리거)`);
    autoTriggers.forEach((trigger, index) => {
      Logger.log(`\n트리거 #${index + 1}:`);
      Logger.log(`  함수: ${trigger.getHandlerFunction()}`);
      Logger.log(`  실행 주기: 1분마다`);
    });
  } else {
    Logger.log("⚠️ 자동 실행 비활성화됨");
    Logger.log("   → setupTimeTrigger() 실행하여 활성화");
  }

  // Script Properties 확인
  const props = PropertiesService.getScriptProperties();
  const lastProcessedRow = props.getProperty('lastProcessedRow');
  const lastProcessedTime = props.getProperty('lastProcessedTime');

  Logger.log("\n📝 마지막 처리 정보:");
  Logger.log(`  행 수: ${lastProcessedRow || '없음'}`);
  Logger.log(`  시간: ${lastProcessedTime || '없음'}`);
  Logger.log("=".repeat(60));

  return {
    active: autoTriggers.length > 0,
    triggerCount: autoTriggers.length,
    lastProcessedRow: lastProcessedRow,
    lastProcessedTime: lastProcessedTime
  };
}


// ============================================================
// UI 헬퍼 함수 (Apps Script 에디터에서 수동 실행용)
// ============================================================

/**
 * UI와 함께 Time Trigger 설정 (Apps Script 에디터에서 수동 실행)
 * setupTimeTrigger()를 호출하고 결과를 UI로 표시
 */
function setupTimeTriggerWithUI() {
  const result = setupTimeTrigger();

  SpreadsheetApp.getUi().alert(
    "✅ 자동 실행 설정 완료!\n\n" +
    "앞으로 Python이 Type 시트에 CSV를 업로드하면\n" +
    "1분 이내에 자동으로 Key Player 마킹이 실행됩니다.\n\n" +
    "확인: Apps Script > 트리거 메뉴"
  );
}


/**
 * UI와 함께 Time Trigger 삭제 (Apps Script 에디터에서 수동 실행)
 */
function deleteTimeTriggerWithUI() {
  const result = deleteTimeTrigger();

  SpreadsheetApp.getUi().alert(
    "✅ 자동 실행 중단 완료!\n\n" +
    result + "\n\n" +
    "다시 활성화하려면 setupTimeTriggerWithUI() 실행"
  );
}


/**
 * UI와 함께 Trigger 상태 확인 (Apps Script 에디터에서 수동 실행)
 */
function checkTriggerStatusWithUI() {
  const status = checkTriggerStatus();

  let message = status.active
    ? `✅ 자동 실행 활성화됨\n\n트리거 수: ${status.triggerCount}개\n실행 주기: 1분마다`
    : "⚠️ 자동 실행 비활성화됨\n\nsetupTimeTriggerWithUI() 실행 필요";

  if (status.lastProcessedTime) {
    message += `\n\n마지막 처리:\n${status.lastProcessedTime}\n행 수: ${status.lastProcessedRow}`;
  }

  SpreadsheetApp.getUi().alert(message);
}