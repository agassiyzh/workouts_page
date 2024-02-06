import { formatSpeed, formatPace, colorFromType, formatRunTime, Activity, titleForRun, RunIds } from '@/utils/utils';
import styles from './style.module.scss';
import { USE_SPEED } from '@/utils/const';

interface IRunRowProperties {
  elementIndex: number;
  locateActivity: (_runIds: RunIds) => void;
  run: Activity;
  runIndex: number;
  setRunIndex: (_ndex: number) => void;
}

const RunRow = ({ elementIndex, locateActivity, run, runIndex, setRunIndex }: IRunRowProperties) => {
  const distance = (run.distance / 1000.0).toFixed(2);
  const paceParts = run.average_speed ? (USE_SPEED? formatSpeed(run.average_speed) :formatPace(run.average_speed)) : null;
  const heartRate = run.average_heartrate;
  const type = run.type;
  const runTime = formatRunTime(run.moving_time);
  const handleClick = () => {
    if (runIndex === elementIndex) {
      setRunIndex(-1);
      locateActivity([]);
      return
    };
    setRunIndex(elementIndex);
    locateActivity([run.run_id]);
  };

  return (
    <tr
      className={`${styles.runRow} ${runIndex === elementIndex ? styles.selected : ''}`}
      key={run.start_date_local}
      onClick={handleClick}
      style={{color: colorFromType(type)}}
    >
      <td>{titleForRun(run)}</td>
      <td>{type}</td>
      <td>{distance}</td>
      {paceParts && <td>{paceParts}</td>}
      <td>{heartRate && heartRate.toFixed(0)}</td>
      <td>{run.cadence}</td>
      <td>{runTime}</td>
      <td className={styles.runDate}>{run.start_date_local}</td>
      <td>{run.source}</td>
    </tr>
  );
};

export default RunRow;
