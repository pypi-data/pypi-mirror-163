from typing import Dict, Any, List

from ..analyses.series import SeriesModel, Series


class SeriesCollection:
    tracking: Dict[str, SeriesModel]
    indicators: set
    step: int
    max_buffer_length: int

    @classmethod
    def defaults(cls):
        return dict(tracking={},
                    step=0,
                    indicators=set(),
                    max_buffer_length=None,
                    )

    def get_tracks(self) -> List[SeriesModel]:
        res = []
        is_series_updated = False
        for ind, track in self.tracking.items():
            name = ind.split('.')

            s = Series().load(track)
            series: Dict[str, Any] = s.detail
            series['name'] = '.'.join(name[1:])

            if s.is_smoothed_updated:
                self.tracking[ind] = s.to_data()
                is_series_updated = True

            res.append(series)

        if is_series_updated:
            self.save()

        return res

    def track(self, data: Dict[str, SeriesModel]) -> None:
        for ind, series in data.items():
            self.step = max(self.step, series['step'][-1])
            self._update_series(ind, series)

        self.save()

    def _update_series(self, ind: str, series: SeriesModel) -> None:
        if ind not in self.tracking:
            self.tracking[ind] = Series(self.max_buffer_length).to_data()

        s = Series(self.max_buffer_length).load(self.tracking[ind])
        s.update(series['step'], series['value'])

        self.tracking[ind] = s.to_data()

    def save(self):
        raise NotImplementedError
