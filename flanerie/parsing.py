import gpxpy

class GPXParser(object):
    def __init__(self, path):
        self._name = None
        self._path = None

        with open(path) as fp:
            self._gpx = gpxpy.parse(fp)

    @property
    def path(self):
        if self._path is None:
            self._path = self._parse_path()
        return self._path

    @property
    def name(self):
        if self._name is None:
            self._name = self._gpx.name
        return self._name

    def _parse_path(self):
        if len(self._gpx.tracks) != 1:
            raise NotImplementedError('Only supporting GPX files with a single track.')

        track  = self._gpx.tracks[0]

        path = []
        for segment in track.segments:
            path.extend([(p.latitude, p.longitude) for p in segment.points])

        return path
